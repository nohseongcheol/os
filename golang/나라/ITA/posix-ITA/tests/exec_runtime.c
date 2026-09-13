#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int numero_di_cifre)
{
    (void)Scrittura(STDOUT_FILENO, text, numero_di_cifre);
}

int main(void)
{
    int stato;
    int descrittore_del_file;
    char *argomenti_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &stato, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&stato) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    descrittore_del_file = Apri("/USER2", O_RDONLY);
    if (descrittore_del_file < 0 || dup2(descrittore_del_file, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (descrittore_del_file != 10)
        (void)Chiudi(descrittore_del_file);

    (void)execve("/PXEXEC", argomenti_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
