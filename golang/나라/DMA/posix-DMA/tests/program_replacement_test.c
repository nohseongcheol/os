#include <errno.h>
#include <fcntl.h>
#include <system/child_wait.h>
#include <unistd.h>

static void write_message(const char *text, unsigned int digit_count)
{
    (void)write(standard_output_descriptor, text, digit_count);
}

int main(void)
{
    int status;
    int file_descriptor;
    char *arguments_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    write_message("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &status, do_not_wait_if_unready) == -1 && errno == no_child_process)
        write_message("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        write_message("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&status) == -1 && errno == no_child_process)
        write_message("PTEST:PASS:wait-echild-empty\n", 29);
    else
        write_message("PTEST:FAIL:wait-echild-empty\n", 29);

    file_descriptor = open("/USER2", open_read_only);
    if (file_descriptor < 0 || dup2(file_descriptor, 10) != 10 || fcntl(10, set_descriptor_flags, close_on_program_replacement) != 0) {
        write_message("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (file_descriptor != 10)
        (void)close(file_descriptor);

    (void)execve("/PXEXEC", arguments_2, envp);
    write_message("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
