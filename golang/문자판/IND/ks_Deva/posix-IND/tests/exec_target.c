#include <errno.h>
#include <fcntl.h>
#include <unistd.h>

static int text_equal(const char *left, const char *right)
{
    unsigned int i = 0;
    while (left[i] != 0 && right[i] != 0) {
        if (left[i] != right[i])
            return 0;
        i++;
    }
    return left[i] == right[i];
}

int main(int argc, char **argv, char **envp)
{
    static const char loaded[] = "PTEST:PASS:exec-image\n";
    static const char args_pass[] = "PTEST:PASS:exec-argv-envp\n";
    static const char args_fail[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)लिखुन(STDOUT_FILENO, loaded, sizeof(loaded) - 1);
    if (argc == 2 && argv != (char **)0 && envp != (char **)0 &&
        argv[0] != (char *)0 && argv[1] != (char *)0 && argv[2] == (char *)0 &&
        envp[0] != (char *)0 && envp[1] == (char *)0 &&
        environ == envp && text_equal(argv[0], "PXEXEC") &&
        text_equal(argv[1], "argument") && text_equal(envp[0], "POSIX_TEST=1")) {
        (void)लिखुन(STDOUT_FILENO, args_pass, sizeof(args_pass) - 1);
    } else {
        (void)लिखुन(STDOUT_FILENO, args_fail, sizeof(args_fail) - 1);
        _exit(38);
    }
    errno = 0;
    if (fcntl(10, F_GETFD) == -1 && errno == EBADF) {
        static const char cloexec_pass[] = "PTEST:PASS:cloexec\n";
        (void)लिखुन(STDOUT_FILENO, cloexec_pass, sizeof(cloexec_pass) - 1);
        _exit(37);
    }
    {
        static const char cloexec_fail[] = "PTEST:FAIL:cloexec\n";
        (void)लिखुन(STDOUT_FILENO, cloexec_fail, sizeof(cloexec_fail) - 1);
    }
    _exit(39);
}
