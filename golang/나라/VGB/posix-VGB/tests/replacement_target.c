#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

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

int main(int argument_count, char **arguments_2, char **envp)
{
    static const char loaded_value[] = "PTEST:PASS:exec-image\n";
    static const char argument_test_success[] = "PTEST:PASS:exec-argv-envp\n";
    static const char argument_test_failure[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)write(standard_output_descriptor, loaded_value, sizeof(loaded_value) - 1);
    if (argument_count == 2 && arguments_2 != (char **)0 && envp != (char **)0 &&
        arguments_2[0] != (char *)0 && arguments_2[1] != (char *)0 && arguments_2[2] == (char *)0 &&
        envp[0] != (char *)0 && envp[1] == (char *)0 &&
        environ == envp && text_is_equal(arguments_2[0], "PXEXEC") &&
        text_is_equal(arguments_2[1], "argument") && text_is_equal(envp[0], "POSIX_TEST=1")) {
        (void)write(standard_output_descriptor, argument_test_success, sizeof(argument_test_success) - 1);
    } else {
        (void)write(standard_output_descriptor, argument_test_failure, sizeof(argument_test_failure) - 1);
        _exit(38);
    }
    errno = 0;
    if (fcntl(10, read_descriptor_flags) == -1 && errno == invalid_file_descriptor) {
        static const char close_on_exec_success[] = "PTEST:PASS:cloexec\n";
        (void)write(standard_output_descriptor, close_on_exec_success, sizeof(close_on_exec_success) - 1);
        _exit(37);
    }
    {
        static const char close_on_exec_failure[] = "PTEST:FAIL:cloexec\n";
        (void)write(standard_output_descriptor, close_on_exec_failure, sizeof(close_on_exec_failure) - 1);
    }
    _exit(39);
}
