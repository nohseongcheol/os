/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <system/child_wait.h>
#include <fcntl.h>
#include <unistd.h>

static void write_message(const char *text, unsigned int digit_count)
{
    (void)write(standard_output_descriptor, text, digit_count);
}

int main(void)
{
    int status;
    process_identifier_type parent_process = getpid();
    process_identifier_type child;
    process_identifier_type waited_process;
    volatile int process_private_value = 10;
    int file_descriptor;
    char byte_value;
    int iteration_number;

    write_message("\nPOSIX-FORK:START\n", 18);
    child = fork();
    if (child == 0) {
        process_private_value = 20;
        if (getppid() != parent_process || process_private_value != 20)
            _exit(90);
        _exit(23);
    }
    if (child < 0) {
        write_message("PTEST:FAIL:fork-return\n", 23);
        _exit(1);
    }
    write_message("PTEST:PASS:fork-return\n", 23);
    waited_process = waitpid(child, &status, 0);
    if (waited_process == child && exited_normally(status) && extract_exit_status(status) == 23 &&
        process_private_value == 10) {
        write_message("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        write_message("PTEST:FAIL:fork-wait-exit\n", 26);
        _exit(1);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    waited_process = wait(&status);
    if (waited_process == child && exited_normally(status) && extract_exit_status(status) == 29)
        write_message("PTEST:PASS:blocking-wait\n", 25);
    else {
        write_message("PTEST:FAIL:blocking-wait\n", 25);
        _exit(1);
    }

    file_descriptor = open("/USER2", open_read_only);
    child = fork();
    if (child == 0) {
        (void)close(file_descriptor);
        _exit(0);
    }
    waited_process = waitpid(child, &status, 0);
    if (file_descriptor >= 0 && waited_process == child && read(file_descriptor, &byte_value, 1) == 1 &&
        (unsigned char)byte_value == 0x7f)
        write_message("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        write_message("PTEST:FAIL:fork-fd-isolation\n", 29);
        _exit(1);
    }
    (void)close(file_descriptor);

    for (iteration_number = 0; iteration_number < 2; iteration_number++) {
        child = fork();
        if (child == 0)
            _exit(iteration_number);
        if (child < 0 || waitpid(child, &status, 0) != child ||
            !exited_normally(status) || extract_exit_status(status) != iteration_number) {
            write_message("PTEST:FAIL:fork-stress\n", 23);
            _exit(1);
        }
    }
    write_message("PTEST:PASS:fork-stress\n", 23);
    write_message("POSIX-FORK:PASS\n", 16);
    _exit(0);
}
