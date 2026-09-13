#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int liczba_cyfr)
{
    (void)Zapis(STDOUT_FILENO, text, liczba_cyfr);
}

int main(void)
{
    int stan;
    int deskryptor_pliku;
    char *argumenty_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &stan, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&stan) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    deskryptor_pliku = Otwórz("/USER2", O_RDONLY);
    if (deskryptor_pliku < 0 || dup2(deskryptor_pliku, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (deskryptor_pliku != 10)
        (void)Zamknij(deskryptor_pliku);

    (void)execve("/PXEXEC", argumenty_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
