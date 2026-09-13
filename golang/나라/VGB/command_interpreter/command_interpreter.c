#include <network_conversion/byte_order.h>
#include <errno.h>
#include <fcntl.h>
#include <internetwork/address.h>
#include <basic_definitions.h>
#include <system/socket.h>
#include <system/stat.h>
#include <system/system_identity.h>
#include <system/child_wait.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { input_line_capacity = 512, maximum_argument_count = 16, maximum_script_nesting = 4 };
static int script_nesting_depth;
struct input_stream {
    int input_descriptor;
    char transfer_buffer_2[256];
    object_size_type position;
    object_size_type length;
};

static object_size_type text_byte_length(const char *text)
{
    object_size_type length = 0;
    while (text[length] != '\0')
        length++;
    return length;
}

static int texts_equal(const char *left, const char *right)
{
    object_size_type position = 0;
    while (left[position] == right[position]) {
        if (left[position] == '\0')
            return 1;
        position++;
    }
    return 0;
}

static void write_text(const char *text)
{
    object_size_type length = text_byte_length(text);
    while (length > 0U) {
        signed_size_type written_byte_count = write(standard_output_descriptor, text, length);
        if (written_byte_count <= 0)
            return;
        text += written_byte_count;
        length -= (object_size_type)written_byte_count;
    }
}

static void write_integer(int value)
{
    char digit_characters[16];
    unsigned int digit_count;
    unsigned int unsigned_magnitude;

    if (value < 0) {
        write_text("-");
        unsigned_magnitude = (unsigned int)(-(value + 1)) + 1U;
    } else {
        unsigned_magnitude = (unsigned int)value;
    }
    digit_count = 0;
    do {
        digit_characters[digit_count++] = (char)('0' + unsigned_magnitude % 10U);
        unsigned_magnitude /= 10U;
    } while (unsigned_magnitude != 0U);
    while (digit_count > 0U) {
        digit_count--;
        (void)write(standard_output_descriptor, &digit_characters[digit_count], 1);
    }
}

static void report_error(const char *operation)
{
    write_text("error: ");
    write_text(operation);
    write_text(" errno=");
    write_integer(errno);
    write_text("\n");
}

static int read_input_line(struct input_stream *input, char *input_line, object_size_type capacity)
{
    object_size_type position = 0;
    int invalid_input_line = 0;
    char character;
    signed_size_type bytes_read;
    if (capacity < 2U)
        return -2;
    for (;;) {
        if (input->position == input->length) {
            bytes_read = read(input->input_descriptor, input->transfer_buffer_2, sizeof(input->transfer_buffer_2));
            if (bytes_read < 0) {
                if (errno == operation_interrupted)
                    continue;
                return -1;
            }
            if (bytes_read == 0) {
                if (position == 0 && !invalid_input_line)
                    return -1;
                break;
            }
            input->length = (object_size_type)bytes_read;
            input->position = 0;
        }
        character = input->transfer_buffer_2[input->position++];
        if (character == '\n')
            break;
        if (input->input_descriptor == standard_input_descriptor && character == 4) {
            if (position == 0 && !invalid_input_line)
                return -1;
            break;
        }
        if (input->input_descriptor == standard_input_descriptor && (character == 8 || character == 127)) {
            if (position > 0) {
                do {
                    position--;
                } while (position > 0 && ((unsigned char)input_line[position] & 0xc0U) == 0x80U);
            }
            continue;
        }
        if (character == '\r')
            continue;
        if (character == '\0') {
            invalid_input_line = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (position + 1U < capacity)
            input_line[position++] = character;
        else
            invalid_input_line = 1;
    }
    input_line[position] = '\0';
    return invalid_input_line ? -2 : (int)position;
}

static int split_arguments(char *input_line, char **arguments)
{
    int argument_count = 0;
    char *current = input_line;
    char *output = input_line;

    while (*current != '\0') {
        char quote = '\0';
        while (*current == ' ' || *current == '\t')
            current++;
        if (*current == '\0' || *current == '#')
            break;
        if (argument_count == maximum_argument_count - 1)
            return -1;
        arguments[argument_count++] = output;
        while (*current != '\0') {
            char character = *current++;
            if (quote == '\0' && (character == ' ' || character == '\t'))
                break;
            if (character == '\\' && quote != '\'') {
                if (*current == '\0')
                    return -1;
                *output++ = *current++;
            } else if (character == '\'' || character == '"') {
                if (quote == '\0')
                    quote = character;
                else if (quote == character)
                    quote = '\0';
                else
                    *output++ = character;
            } else {
                *output++ = character;
            }
        }
        if (quote != '\0')
            return -1;
        *output++ = '\0';
    }
    arguments[argument_count] = (char *)0;
    return argument_count;
}

static void show_help(void)
{
    object_size_type position;
    write_text(
        "WorldOS command interpreter commands:\n"
        "  help                 show this help\n"
        "  echo TEXT            print text\n"
        "  pwd                  show current directory\n"
        "  cd PATH              change directory\n"
        "  cat FILE             print a FAT file\n"
        "  stat FILE            show file size\n"
        "  pid                  show process identifiers\n"
        "  uname                show operating-system identity\n"
        "  run FILE [ARGS...]   execute a user ELF program\n"
        "  udp [TEXT]           call POSIX UDP and loop back TEXT\n"
        "  source FILE          interpret a UTF-8 command file\n"
        "  exit                 leave the shell\n");
    write_text("Native command proposals (ASCII aliases remain available):\n");
    for (position = 0; position < sizeof(canonical_commands) / sizeof(canonical_commands[0]); position++) {
        write_text(native_command_aliases[position]);
        write_text(" = ");
        write_text(canonical_commands[position]);
        write_text("\n");
    }
}

static int command_matches(const char *text, const char *command)
{
    object_size_type position;
    if (texts_equal(text, command))
        return 1;
    for (position = 0; position < sizeof(canonical_commands) / sizeof(canonical_commands[0]); position++)
        if (texts_equal(command, canonical_commands[position]))
            return texts_equal(text, native_command_aliases[position]);
    return 0;
}

static int interpret_input(int input_descriptor);

static int interpret_command_file(const char *file_name)
{
    int file_descriptor;
    int status;
    if (script_nesting_depth >= maximum_script_nesting) {
        write_text("source: nesting limit\n");
        return 0;
    }
    file_descriptor = open(file_name, open_read_only);
    if (file_descriptor < 0) {
        report_error(file_name);
        return 0;
    }
    script_nesting_depth++;
    status = interpret_input(file_descriptor);
    script_nesting_depth--;
    (void)close(file_descriptor);
    return status;
}

static void print_arguments(int argument_count, char **arguments)
{
    int position;
    for (position = 1; position < argument_count; position++) {
        if (position != 1)
            write_text(" ");
        write_text(arguments[position]);
    }
    write_text("\n");
}

static void show_working_directory(void)
{
    char path[128];
    if (getcwd(path, sizeof(path)) == (char *)0) {
        report_error("pwd");
        return;
    }
    write_text(path);
    write_text("\n");
}

static void display_file_contents(const char *file_name)
{
    char transfer_buffer_2[128];
    int file_descriptor = open(file_name, open_read_only);
    signed_size_type bytes_read;

    if (file_descriptor < 0) {
        report_error("cat");
        return;
    }
    while ((bytes_read = read(file_descriptor, transfer_buffer_2, sizeof(transfer_buffer_2))) > 0)
        (void)write(standard_output_descriptor, transfer_buffer_2, (object_size_type)bytes_read);
    if (bytes_read < 0)
        report_error("cat/read");
    (void)close(file_descriptor);
    write_text("\n");
}

static void show_file_information(const char *file_name)
{
    struct stat status;
    if (stat(file_name, &status) < 0) {
        report_error("stat");
        return;
    }
    write_text("size=");
    write_integer((int)status.file_size);
    write_text(is_directory_mode(status.file_kind_and_permissions) ? " type=directory\n" : " type=file\n");
}

static void show_process_identifiers(void)
{
    write_text("pid=");
    write_integer((int)getpid());
    write_text(" ppid=");
    write_integer((int)getppid());
    write_text("\n");
}

static void show_system_identity(void)
{
    struct system_identity_2 system_identity;
    if (uname(&system_identity) < 0) {
        report_error("uname");
        return;
    }
    write_text(system_identity.system_name);
    write_text(" ");
    write_text(system_identity.system_release);
    write_text(" ");
    write_text(system_identity.machine_kind);
    write_text("\n");
}

static void run_program(int argument_count, char **arguments)
{
    process_identifier_type child_process_identifier;
    int child_termination_status = 0;

    if (argument_count < 2) {
        write_text("usage: run FILE [ARGS...]\n");
        return;
    }
    child_process_identifier = fork();
    if (child_process_identifier < 0) {
        report_error("fork");
        return;
    }
    if (child_process_identifier == 0) {
        execve(arguments[1], &arguments[1], (char *const *)0);
        report_error("execve");
        _exit(127);
    }
    if (waitpid(child_process_identifier, &child_termination_status, 0) < 0) {
        report_error("waitpid");
        return;
    }
    write_text("exit-status=");
    write_integer(extract_exit_status(child_termination_status));
    write_text("\n");
}

static void test_datagram_loopback(const char *message)
{
    struct internetwork_endpoint_address receiving_endpoint_address = {0};
    struct internetwork_endpoint_address sender_endpoint_address = {0};
    address_length_type sender_address_length = sizeof(sender_endpoint_address);
    char received_data[96];
    object_size_type message_byte_length = text_byte_length(message);
    int receiving_socket = -1;
    int sending_socket = -1;
    signed_size_type received_byte_count;

    if (message_byte_length >= sizeof(received_data)) {
        write_text("udp: message exceeds 95 bytes\n");
        return;
    }
    receiving_socket = socket(internetwork_address_family_code, datagram_endpoint, user_datagram_protocol);
    sending_socket = socket(internetwork_address_family_code, datagram_endpoint, user_datagram_protocol);
    if (receiving_socket < 0 || sending_socket < 0) {
        report_error("socket");
        goto close_sockets;
    }
    receiving_endpoint_address.internetwork_address_family = internetwork_address_family_code;
    receiving_endpoint_address.transport_port_number = htons(40404);
    receiving_endpoint_address.internetwork_address_field.address_value = htonl(loopback_address);
    if (bind(receiving_socket, (const struct endpoint_address *)&receiving_endpoint_address, sizeof(receiving_endpoint_address)) < 0) {
        report_error("bind");
        goto close_sockets;
    }
    if (connect(sending_socket, (const struct endpoint_address *)&receiving_endpoint_address, sizeof(receiving_endpoint_address)) < 0) {
        report_error("connect");
        goto close_sockets;
    }
    if (send(sending_socket, message, message_byte_length, 0) != (signed_size_type)message_byte_length) {
        report_error("send");
        goto close_sockets;
    }
    received_byte_count = recvfrom(receiving_socket, received_data, sizeof(received_data) - 1U, 0,
                         (struct endpoint_address *)&sender_endpoint_address, &sender_address_length);
    if (received_byte_count < 0) {
        report_error("recvfrom");
        goto close_sockets;
    }
    received_data[received_byte_count] = '\0';
    write_text("udp-received: ");
    write_text(received_data);
    write_text("\n");

close_sockets:
    if (sending_socket >= 0)
        (void)close(sending_socket);
    if (receiving_socket >= 0)
        (void)close(receiving_socket);
}

static int interpret_input(int input_descriptor)
{
    char input_line[input_line_capacity];
    char *arguments[maximum_argument_count];
    struct input_stream input = {0};
    input.input_descriptor = input_descriptor;

    for (;;) {
        int argument_count;
        int status;
        if (input_descriptor == standard_input_descriptor)
            write_text("worldos$ ");
        status = read_input_line(&input, input_line, sizeof(input_line));
        if (status == -1)
            return 0;
        if (status == -2) {
            write_text("input rejected: overlong or binary line\n");
            continue;
        }
        argument_count = split_arguments(input_line, arguments);
        if (argument_count < 0) {
            write_text("syntax error: quote, escape or argument limit\n");
            continue;
        }
        if (argument_count == 0)
            continue;
        if (command_matches(arguments[0], "help"))
            show_help();
        else if (command_matches(arguments[0], "echo"))
            print_arguments(argument_count, arguments);
        else if (command_matches(arguments[0], "pwd"))
            show_working_directory();
        else if (command_matches(arguments[0], "cd")) {
            if (argument_count < 2)
                write_text("usage: cd PATH\n");
            else if (chdir(arguments[1]) < 0)
                report_error("cd");
        } else if (command_matches(arguments[0], "cat")) {
            if (argument_count < 2)
                write_text("usage: cat FILE\n");
            else
                display_file_contents(arguments[1]);
        } else if (command_matches(arguments[0], "stat")) {
            if (argument_count < 2)
                write_text("usage: stat FILE\n");
            else
                show_file_information(arguments[1]);
        } else if (command_matches(arguments[0], "pid"))
            show_process_identifiers();
        else if (command_matches(arguments[0], "uname"))
            show_system_identity();
        else if (command_matches(arguments[0], "run"))
            run_program(argument_count, arguments);
        else if (command_matches(arguments[0], "udp"))
            test_datagram_loopback(argument_count >= 2 ? arguments[1] : "ping");
        else if (command_matches(arguments[0], "source")) {
            if (argument_count < 2)
                write_text("usage: source FILE\n");
            else if (interpret_command_file(arguments[1]))
                return 1;
        } else if (command_matches(arguments[0], "exit"))
            return 1;
        else
            write_text("unknown command; type help\n");
    }
}

int main(void)
{
    write_text("WORLDOS-SHELL:READY\n");
    (void)interpret_input(standard_input_descriptor);
    write_text("WORLDOS-SHELL:EXIT\n");
    return 0;
}
