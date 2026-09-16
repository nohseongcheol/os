/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <system/stat.h>
#include <system/system_identity.h>
#include <system/child_wait.h>
#include <unistd.h>

static int check_count;
static int failure_count;

static unsigned int text_byte_length(const char *text)
{
    unsigned int length = 0;
    while (text[length] != 0)
        length++;
    return length;
}

static int text_is_equal(const char *left, const char *right)
{
    unsigned int item_index = 0;
    while (left[item_index] != 0 && right[item_index] != 0) {
        if (left[item_index] != right[item_index])
            return 0;
        item_index++;
    }
    return left[item_index] == right[item_index];
}

static void write_message(const char *text)
{
    (void)write(standard_output_descriptor, text, text_byte_length(text));
}

static void report_result(const char *system_identity, int passed_test)
{
    check_count++;
    if (passed_test) {
        write_message("PTEST:PASS:");
    } else {
        failure_count++;
        write_message("PTEST:FAIL:");
    }
    write_message(system_identity);
    write_message("\n");
}

static int failed_with_error(int result, int expected_error_number)
{
    return result == -1 && errno == expected_error_number;
}

static process_identifier_type reap_without_waiting(process_identifier_type child, int *status)
{
    unsigned int spin_count;
    process_identifier_type result;

    for (spin_count = 0; spin_count < 2000000U; spin_count++) {
        result = waitpid(child, status, do_not_wait_if_unready);
        if (result != 0)
            return result;
    }
    return 0;
}

static void test_process_identity(void)
{
    report_result("getpid", getpid() > 0);
    report_result("getppid", getppid() >= 0);
    report_result("getuid", getuid() == 0);
    report_result("geteuid", geteuid() == 0);
    report_result("getgid", getgid() == 0);
    report_result("getegid", getegid() == 0);
}

static void test_path_operations(void)
{
    char working_directory[4] = {'x', 'x', 'x', 'x'};
    struct stat st;

    report_result("getcwd", getcwd(working_directory, sizeof(working_directory)) == working_directory && working_directory[0] == '/' && working_directory[1] == 0);
    errno = 0;
    report_result("getcwd-erange", getcwd(working_directory, 1) == 0 && errno == value_out_of_range);
    errno = 0;
    report_result("getcwd-efault", getcwd((char *)0, 4) == 0 && errno == invalid_memory_address);

    report_result("chdir-root", chdir("/") == 0);
    report_result("chdir-dot", chdir(".") == 0);
    report_result("chdir-root-dot", chdir("/.") == 0);
    errno = 0;
    report_result("chdir-enotdir", failed_with_error(chdir("/USER2"), not_a_directory));
    errno = 0;
    report_result("chdir-efault", failed_with_error(chdir((const char *)0), invalid_memory_address));

    report_result("access-file", access("/USER2", test_existence) == 0 && access("/USER2", test_read_permission) == 0);
    report_result("access-root", access("/", test_existence | test_read_permission | test_execute_permission) == 0);
    errno = 0;
    report_result("access-write-denied", failed_with_error(access("/USER2", test_write_permission), permission_denied));
    errno = 0;
    report_result("access-execute-denied", failed_with_error(access("/USER2", test_execute_permission), permission_denied));
    errno = 0;
    report_result("access-enoent", failed_with_error(access("/NOFILE", test_existence), file_or_directory_missing));
    errno = 0;
    report_result("access-einval", failed_with_error(access("/USER2", 8), invalid_argument));
    errno = 0;
    report_result("access-efault", failed_with_error(access((const char *)0, test_existence), invalid_memory_address));

    report_result("stat-root", stat("/", &st) == 0 && is_directory_mode(st.file_kind_and_permissions) && st.hard_link_count == 1);
    report_result("stat-file", stat("/USER2", &st) == 0 && is_regular_file_mode(st.file_kind_and_permissions) && st.file_size > 2);
    report_result("lstat-file", lstat("/USER2", &st) == 0 && is_regular_file_mode(st.file_kind_and_permissions));
    errno = 0;
    report_result("stat-enoent", failed_with_error(stat("/NOFILE", &st), file_or_directory_missing));
    errno = 0;
    report_result("stat-efault-path", failed_with_error(stat((const char *)0, &st), invalid_memory_address));
    errno = 0;
    report_result("stat-efault-buffer", failed_with_error(stat("/", (struct stat *)0), invalid_memory_address));
}

static void test_open_and_io(void)
{
    char byte_array[4];
    struct stat st;
    int file_descriptor;
    int root_path;

    file_descriptor = open("/USER2", open_read_only);
    report_result("open-readonly", file_descriptor >= 3);
    if (file_descriptor >= 0) {
        report_result("read-bytes", read(file_descriptor, byte_array, 2) == 2 &&
               (unsigned char)byte_array[0] == 0x7f && byte_array[1] == 'E');
        report_result("lseek-set", lseek(file_descriptor, 0, offset_from_start) == 0);
        report_result("lseek-cur", lseek(file_descriptor, 1, offset_from_current) == 1);
        report_result("lseek-end", lseek(file_descriptor, -1, offset_from_end) > 0);
        errno = 0;
        report_result("lseek-negative", lseek(file_descriptor, -1, offset_from_start) == -1 && errno == invalid_argument);
        errno = 0;
        report_result("lseek-whence", lseek(file_descriptor, 0, 99) == -1 && errno == invalid_argument);
        report_result("fstat-file", fstat(file_descriptor, &st) == 0 && is_regular_file_mode(st.file_kind_and_permissions) && st.file_size > 2);
        errno = 0;
        report_result("fstat-efault", failed_with_error(fstat(file_descriptor, (struct stat *)0), invalid_memory_address));
        report_result("fsync-file", fsync(file_descriptor) == 0);
        report_result("close-file", close(file_descriptor) == 0);
        errno = 0;
        report_result("closed-fd", failed_with_error(close(file_descriptor), invalid_file_descriptor));
    }

    root_path = open("/", open_read_only | require_directory);
    report_result("open-directory", root_path >= 3);
    if (root_path >= 0) {
        report_result("fstat-directory", fstat(root_path, &st) == 0 && is_directory_mode(st.file_kind_and_permissions));
        errno = 0;
        report_result("read-directory", read(root_path, byte_array, 1) == -1 && errno == is_a_directory);
        (void)close(root_path);
    }

    report_result("fstat-character", fstat(standard_output_descriptor, &st) == 0 && is_character_device_mode(st.file_kind_and_permissions));
    report_result("write", write(standard_output_descriptor, "", 0) == 0);
    report_result("read-zero", read(standard_input_descriptor, byte_array, 0) == 0);
    errno = 0;
    report_result("read-ebadf", read(standard_output_descriptor, byte_array, 1) == -1 && errno == invalid_file_descriptor);
    errno = 0;
    report_result("write-ebadf", write(-1, byte_array, 1) == -1 && errno == invalid_file_descriptor);
    errno = 0;
    report_result("lseek-espipe", lseek(standard_output_descriptor, 0, offset_from_start) == -1 && errno == cannot_seek_stream);
    errno = 0;
    report_result("fsync-ebadf", failed_with_error(fsync(-1), invalid_file_descriptor));

    errno = 0;
    report_result("open-enoent", failed_with_error(open("/NOFILE", open_read_only), file_or_directory_missing));
    errno = 0;
    report_result("open-efault", failed_with_error(open((const char *)0, open_read_only), invalid_memory_address));
    errno = 0;
    report_result("open-write-erofs", failed_with_error(open("/USER2", open_write_only), read_only_filesystem));
    errno = 0;
    report_result("open-rdwr-erofs", failed_with_error(open("/USER2", open_read_write), read_only_filesystem));
    errno = 0;
    report_result("open-create-erofs", failed_with_error(open("/NEWFILE", create_if_missing | open_write_only, 0600), read_only_filesystem));
    errno = 0;
    report_result("open-trunc-erofs", failed_with_error(open("/USER2", truncate_existing_file | open_read_only), read_only_filesystem));
    errno = 0;
    report_result("open-append-erofs", failed_with_error(open("/USER2", append_at_end | open_read_only), read_only_filesystem));
    errno = 0;
    report_result("open-enotdir", failed_with_error(open("/USER2", open_read_only | require_directory), not_a_directory));
    errno = 0;
    report_result("creat-erofs", failed_with_error(creat("/NEWFILE", 0600), read_only_filesystem));
    errno = 0;
    report_result("close-ebadf", failed_with_error(close(-1), invalid_file_descriptor));

    sync();
    report_result("sync", 1);
}

static void test_descriptor_duplication_and_control(void)
{
    char first_item;
    char second_item;
    struct stat st;
    int file_descriptor = open("/USER2", open_read_only);
    int copied_value;
    int high;
    int target_value;

    if (file_descriptor < 0) {
        report_result("dup-setup", 0);
        return;
    }
    copied_value = dup(file_descriptor);
    report_result("dup", copied_value >= 0 && copied_value != file_descriptor);
    if (copied_value >= 0) {
        report_result("dup-shared-offset", read(file_descriptor, &first_item, 1) == 1 && read(copied_value, &second_item, 1) == 1 &&
               (unsigned char)first_item == 0x7f && second_item == 'E');
        report_result("dup-close-original", close(file_descriptor) == 0 && fstat(copied_value, &st) == 0);
        file_descriptor = copied_value;
    }

    target_value = dup2(file_descriptor, 20);
    report_result("dup2", target_value == 20 && fstat(20, &st) == 0);
    report_result("dup2-same", dup2(file_descriptor, file_descriptor) == file_descriptor);
    if (target_value == 20)
        (void)close(20);
    errno = 0;
    report_result("dup2-old-ebadf", failed_with_error(dup2(-1, 10), invalid_file_descriptor));
    errno = 0;
    report_result("dup2-new-ebadf", failed_with_error(dup2(file_descriptor, 99), invalid_file_descriptor));

    report_result("fcntl-getfd", fcntl(file_descriptor, read_descriptor_flags) == 0);
    report_result("fcntl-setfd", fcntl(file_descriptor, set_descriptor_flags, close_on_program_replacement) == 0 &&
           fcntl(file_descriptor, read_descriptor_flags) == close_on_program_replacement);
    high = fcntl(file_descriptor, duplicate_descriptor, 10);
    report_result("fcntl-dupfd", high >= 10);
    if (high >= 0) {
        report_result("fcntl-fd-flags-independent", fcntl(high, read_descriptor_flags) == 0);
        (void)close(high);
    }
    report_result("fcntl-getfl", (fcntl(file_descriptor, read_file_status_flags) & access_mode_mask) == open_read_only);
    report_result("fcntl-setfl", fcntl(file_descriptor, set_file_status_flags, append_at_end) == 0 &&
           (fcntl(file_descriptor, read_file_status_flags) & append_at_end) != 0);
    errno = 0;
    report_result("fcntl-command-einval", failed_with_error(fcntl(file_descriptor, 999), invalid_argument));
    errno = 0;
    report_result("fcntl-fd-ebadf", failed_with_error(fcntl(-1, read_descriptor_flags), invalid_file_descriptor));
    errno = 0;
    report_result("dup-ebadf", failed_with_error(dup(-1), invalid_file_descriptor));
    (void)close(file_descriptor);
}

static void test_terminal_and_system_identity(void)
{
    struct system_identity_2 system_identity;
    int file_descriptor;

    report_result("isatty-stdin", isatty(standard_input_descriptor) == 1);
    report_result("isatty-stdout", isatty(standard_output_descriptor) == 1);
    file_descriptor = open("/USER2", open_read_only);
    if (file_descriptor >= 0) {
        errno = 0;
        report_result("isatty-enotty", isatty(file_descriptor) == 0 && errno == inappropriate_device_operation);
        (void)close(file_descriptor);
    } else {
        report_result("isatty-enotty", 0);
    }
    errno = 0;
    report_result("isatty-ebadf", isatty(-1) == 0 && errno == invalid_file_descriptor);

    report_result("uname", uname(&system_identity) == 0 && system_identity.system_name[0] != 0 &&
           system_identity.node_name[0] != 0 && text_is_equal(system_identity.machine_kind, "i386"));
    errno = 0;
    report_result("uname-efault", failed_with_error(uname((struct system_identity_2 *)0), invalid_memory_address));
}

void heap_behavior_test(void)
{
    volatile unsigned char *starting_position = (volatile unsigned char *)sbrk(0);
    volatile unsigned char *previous_value;

    report_result("sbrk-query", starting_position != (void *)-1 && starting_position != (void *)0);
    previous_value = (volatile unsigned char *)sbrk(32);
    report_result("sbrk-grow", previous_value == starting_position && sbrk(0) == (void *)(starting_position + 32));
    if (previous_value != (void *)-1) {
        previous_value[0] = 0x5a;
        previous_value[31] = 0xa5;
        report_result("sbrk-memory", previous_value[0] == 0x5a && previous_value[31] == 0xa5);
    }
    report_result("brk-restore", brk((void *)starting_position) == 0 && sbrk(0) == (void *)starting_position);
}

void process_behavior_test(void)
{
    int status = 0;
    int file_descriptor;
    char byte_value;
    process_identifier_type parent_process = getpid();
    process_identifier_type child = fork();
    process_identifier_type waited_process;

    if (child == 0) {
        if (getpid() == parent_process || getppid() != parent_process)
            _exit(90);
        _exit(23);
    }
    report_result("fork", child > 0);
    if (child > 0) {
        waited_process = reap_without_waiting(child, &status);
        report_result("waitpid", waited_process == child && exited_normally(status) && extract_exit_status(status) == 23);
        errno = 0;
        report_result("waitpid-echild", waitpid(child, &status, do_not_wait_if_unready) == -1 && errno == no_child_process);
    }

    file_descriptor = open("/USER2", open_read_only);
    child = fork();
    if (child == 0) {
        (void)close(file_descriptor);
        _exit(0);
    }
    if (child > 0 && reap_without_waiting(child, &status) == child) {
        report_result("fork-fd-isolation", read(file_descriptor, &byte_value, 1) == 1 && (unsigned char)byte_value == 0x7f);
    } else {
        report_result("fork-fd-isolation", 0);
    }
    if (file_descriptor >= 0)
        (void)close(file_descriptor);

    errno = 0;
    report_result("execve-enoent", failed_with_error(execve("/NOFILE", (char *const *)0,
                                                (char *const *)0), file_or_directory_missing));
    errno = 0;
    report_result("execve-efault", failed_with_error(execve((const char *)0, (char *const *)0,
                                                (char *const *)0), invalid_memory_address));

    child = fork();
    if (child == 0) {
        (void)execve("/PXEXEC", (char *const *)0, (char *const *)0);
        _exit(91);
    }
    report_result("execve-fork", child > 0);
    if (child > 0) {
        waited_process = reap_without_waiting(child, &status);
        report_result("execve", waited_process == child && exited_normally(status) && extract_exit_status(status) == 37);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    report_result("wait-fork", child > 0);
    if (child > 0) {
        unsigned int spin_iteration;
        for (spin_iteration = 0; spin_iteration < 2000000U; spin_iteration++)
            (void)getpid();
        waited_process = wait(&status);
        report_result("wait", waited_process == child && exited_normally(status) && extract_exit_status(status) == 29);
    }
}

int main(void)
{
    int uninitialized_data_was_zeroed = check_count == 0 && failure_count == 0;
    check_count = 0;
    failure_count = 0;
    write_message("\nPOSIX-CORE:START\n");
    report_result("bss-zero", uninitialized_data_was_zeroed);
    test_process_identity();
    test_path_operations();
    test_open_and_io();
    test_descriptor_duplication_and_control();
    test_terminal_and_system_identity();
    report_result("suite-completed", check_count > 60);
    if (failure_count == 0)
        write_message("POSIX-CORE:PASS\n");
    else
        write_message("POSIX-CORE:FAIL\n");
    _exit(failure_count == 0 ? 0 : 1);
}
