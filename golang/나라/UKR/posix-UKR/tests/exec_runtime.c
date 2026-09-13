#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int кількість_цифр)
{
    (void)Запис(STDOUT_FILENO, text, кількість_цифр);
}

int main(void)
{
    int стан;
    int дескриптор_файла;
    char *аргументи_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &стан, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&стан) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    дескриптор_файла = Відкрити("/USER2", O_RDONLY);
    if (дескриптор_файла < 0 || dup2(дескриптор_файла, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (дескриптор_файла != 10)
        (void)Закрити(дескриптор_файла);

    (void)execve("/PXEXEC", аргументи_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
