#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int aantal_cijfers)
{
    (void)Schrijven(STDOUT_FILENO, text, aantal_cijfers);
}

int main(void)
{
    int toestand;
    int bestandsdescriptor;
    char *argumenten_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &toestand, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&toestand) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    bestandsdescriptor = Openen("/USER2", O_RDONLY);
    if (bestandsdescriptor < 0 || dup2(bestandsdescriptor, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (bestandsdescriptor != 10)
        (void)Sluiten(bestandsdescriptor);

    (void)execve("/PXEXEC", argumenten_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
