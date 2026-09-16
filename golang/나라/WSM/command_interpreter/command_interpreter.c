/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stddef.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/wait.h>
#include <unistd.h>
#include "shell_locale.h"

/* Adapted from koros4's request interpreter. Private names are localized
 * in each WorldOS edition; main and POSIX ABI names remain unchanged. */

enum { INPUT_LINE_CAPACITY = 512, MAX_ARGUMENT_COUNT = 16, MAX_SCRIPT_DEPTH = 4 };
static int script_depth;
struct input_stream {
    int input_descriptor;
    char buffer[256];
    size_t position;
    size_t length;
};

static size_t text_length(const char *text)
{
    size_t length = 0;
    while (text[length] != '\0')
        length++;
    return length;
}

static int text_equal(const char *left, const char *right)
{
    size_t position = 0;
    while (left[position] == right[position]) {
        if (left[position] == '\0')
            return 1;
        position++;
    }
    return 0;
}

static void write_text(const char *text)
{
    size_t length = text_length(text);
    while (length > 0U) {
        ssize_t bytes_written = tusi(STDOUT_FILENO, text, length);
        if (bytes_written <= 0)
            return;
        text += bytes_written;
        length -= (size_t)bytes_written;
    }
}

static void write_integer(int value)
{
    char digit_text[16];
    unsigned int size;
    unsigned int number;

    if (value < 0) {
        write_text("-");
        number = (unsigned int)(-(value + 1)) + 1U;
    } else {
        number = (unsigned int)value;
    }
    size = 0;
    do {
        digit_text[size++] = (char)('0' + number % 10U);
        number /= 10U;
    } while (number != 0U);
    while (size > 0U) {
        size--;
        (void)tusi(STDOUT_FILENO, &digit_text[size], 1);
    }
}

static void write_error(const char *operation)
{
    write_text("error: ");
    write_text(operation);
    write_text(" errno=");
    write_integer(errno);
    write_text("\n");
}

static int read_line(struct input_stream *input, char *input_line, size_t capacity)
{
    size_t position = 0;
    int overflow = 0;
    char character;
    ssize_t bytes_read;
    if (capacity < 2U)
        return -2;
    for (;;) {
        if (input->position == input->length) {
            bytes_read = faitau(input->input_descriptor, input->buffer, sizeof(input->buffer));
            if (bytes_read < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            }
            if (bytes_read == 0) {
                if (position == 0 && !overflow)
                    return -1;
                break;
            }
            input->length = (size_t)bytes_read;
            input->position = 0;
        }
        character = input->buffer[input->position++];
        if (character == '\n')
            break;
        if (input->input_descriptor == STDIN_FILENO && character == 4) {
            if (position == 0 && !overflow)
                return -1;
            break;
        }
        if (input->input_descriptor == STDIN_FILENO && (character == 8 || character == 127)) {
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
            overflow = 1; /* Reject binary input; do not execute its prefix. */
            continue;
        }
        if (position + 1U < capacity)
            input_line[position++] = character;
        else
            overflow = 1;
    }
    input_line[position] = '\0';
    return overflow ? -2 : (int)position;
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
        if (argument_count == MAX_ARGUMENT_COUNT - 1)
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

static void print_help(void)
{
    size_t position;
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
    for (position = 0; position < sizeof(command_names) / sizeof(command_names[0]); position++) {
        write_text(command_aliases[position]);
        write_text(" = ");
        write_text(command_names[position]);
        write_text("\n");
    }
}

static int command_matches(const char *text, const char *command)
{
    size_t position;
    if (text_equal(text, command))
        return 1;
    for (position = 0; position < sizeof(command_names) / sizeof(command_names[0]); position++)
        if (text_equal(command, command_names[position]))
            return text_equal(text, command_aliases[position]);
    return 0;
}

static int run_input(int input_descriptor);

static int command_source(const char *file_name)
{
    int file_descriptor;
    int status;
    if (script_depth >= MAX_SCRIPT_DEPTH) {
        write_text("source: nesting limit\n");
        return 0;
    }
    file_descriptor = open(file_name, O_RDONLY);
    if (file_descriptor < 0) {
        write_error(file_name);
        return 0;
    }
    script_depth++;
    status = run_input(file_descriptor);
    script_depth--;
    (void)close(file_descriptor);
    return status;
}

static void command_echo(int argument_count, char **arguments)
{
    int position;
    for (position = 1; position < argument_count; position++) {
        if (position != 1)
            write_text(" ");
        write_text(arguments[position]);
    }
    write_text("\n");
}

static void command_pwd(void)
{
    char path[128];
    if (getcwd(path, sizeof(path)) == (char *)0) {
        write_error("pwd");
        return;
    }
    write_text(path);
    write_text("\n");
}

static void command_cat(const char *file_name)
{
    char buffer[128];
    int file_descriptor = open(file_name, O_RDONLY);
    ssize_t bytes_read;

    if (file_descriptor < 0) {
        write_error("cat");
        return;
    }
    while ((bytes_read = faitau(file_descriptor, buffer, sizeof(buffer))) > 0)
        (void)tusi(STDOUT_FILENO, buffer, (size_t)bytes_read);
    if (bytes_read < 0)
        write_error("cat/read");
    (void)close(file_descriptor);
    write_text("\n");
}

static void command_stat(const char *file_name)
{
    struct stat status;
    if (stat(file_name, &status) < 0) {
        write_error("stat");
        return;
    }
    write_text("size=");
    write_integer((int)status.st_size);
    write_text(S_ISDIR(status.st_mode) ? " type=directory\n" : " type=file\n");
}

static void command_pid(void)
{
    write_text("pid=");
    write_integer((int)getpid());
    write_text(" ppid=");
    write_integer((int)getppid());
    write_text("\n");
}

static void command_uname(void)
{
    struct utsname name;
    if (uname(&name) < 0) {
        write_error("uname");
        return;
    }
    write_text(name.sysname);
    write_text(" ");
    write_text(name.release);
    write_text(" ");
    write_text(name.machine);
    write_text("\n");
}

static void command_run(int argument_count, char **arguments)
{
    pid_t child_pid;
    int wait_status = 0;

    if (argument_count < 2) {
        write_text("usage: run FILE [ARGS...]\n");
        return;
    }
    child_pid = fork();
    if (child_pid < 0) {
        write_error("fork");
        return;
    }
    if (child_pid == 0) {
        execve(arguments[1], &arguments[1], (char *const *)0);
        write_error("execve");
        _exit(127);
    }
    if (waitpid(child_pid, &wait_status, 0) < 0) {
        write_error("waitpid");
        return;
    }
    write_text("exit-status=");
    write_integer(WEXITSTATUS(wait_status));
    write_text("\n");
}

static void command_udp(const char *message)
{
    struct sockaddr_in receive_address = {0};
    struct sockaddr_in source_address = {0};
    socklen_t source_address_length = sizeof(source_address);
    char received_data[96];
    size_t message_length = text_length(message);
    int receive_socket = -1;
    int send_socket = -1;
    ssize_t received_length;

    if (message_length >= sizeof(received_data)) {
        write_text("udp: message exceeds 95 bytes\n");
        return;
    }
    receive_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    send_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (receive_socket < 0 || send_socket < 0) {
        write_error("socket");
        goto cleanup;
    }
    receive_address.sin_family = AF_INET;
    receive_address.sin_port = htons(40404);
    receive_address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(receive_socket, (const struct sockaddr *)&receive_address, sizeof(receive_address)) < 0) {
        write_error("bind");
        goto cleanup;
    }
    if (connect(send_socket, (const struct sockaddr *)&receive_address, sizeof(receive_address)) < 0) {
        write_error("connect");
        goto cleanup;
    }
    if (send(send_socket, message, message_length, 0) != (ssize_t)message_length) {
        write_error("send");
        goto cleanup;
    }
    received_length = recvfrom(receive_socket, received_data, sizeof(received_data) - 1U, 0,
                         (struct sockaddr *)&source_address, &source_address_length);
    if (received_length < 0) {
        write_error("recvfrom");
        goto cleanup;
    }
    received_data[received_length] = '\0';
    write_text("udp-received: ");
    write_text(received_data);
    write_text("\n");

cleanup:
    if (send_socket >= 0)
        (void)close(send_socket);
    if (receive_socket >= 0)
        (void)close(receive_socket);
}

static int run_input(int input_descriptor)
{
    char input_line[INPUT_LINE_CAPACITY];
    char *arguments[MAX_ARGUMENT_COUNT];
    struct input_stream input = {0};
    input.input_descriptor = input_descriptor;

    for (;;) {
        int argument_count;
        int status;
        if (input_descriptor == STDIN_FILENO)
            write_text("worldos$ ");
        status = read_line(&input, input_line, sizeof(input_line));
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
            print_help();
        else if (command_matches(arguments[0], "echo"))
            command_echo(argument_count, arguments);
        else if (command_matches(arguments[0], "pwd"))
            command_pwd();
        else if (command_matches(arguments[0], "cd")) {
            if (argument_count < 2)
                write_text("usage: cd PATH\n");
            else if (chdir(arguments[1]) < 0)
                write_error("cd");
        } else if (command_matches(arguments[0], "cat")) {
            if (argument_count < 2)
                write_text("usage: cat FILE\n");
            else
                command_cat(arguments[1]);
        } else if (command_matches(arguments[0], "stat")) {
            if (argument_count < 2)
                write_text("usage: stat FILE\n");
            else
                command_stat(arguments[1]);
        } else if (command_matches(arguments[0], "pid"))
            command_pid();
        else if (command_matches(arguments[0], "uname"))
            command_uname();
        else if (command_matches(arguments[0], "run"))
            command_run(argument_count, arguments);
        else if (command_matches(arguments[0], "udp"))
            command_udp(argument_count >= 2 ? arguments[1] : "ping");
        else if (command_matches(arguments[0], "source")) {
            if (argument_count < 2)
                write_text("usage: source FILE\n");
            else if (command_source(arguments[1]))
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
    (void)run_input(STDIN_FILENO);
    write_text("WORLDOS-SHELL:EXIT\n");
    return 0;
}
