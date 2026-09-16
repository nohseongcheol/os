/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int numeroiden_määrä)
{
    (void)Kirjoitus(STDOUT_FILENO, text, numeroiden_määrä);
}

int main(void)
{
    int tila;
    int tiedostokuvaaja;
    char *argumentit_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &tila, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&tila) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    tiedostokuvaaja = Avaa("/USER2", O_RDONLY);
    if (tiedostokuvaaja < 0 || dup2(tiedostokuvaaja, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (tiedostokuvaaja != 10)
        (void)Sulje(tiedostokuvaaja);

    (void)execve("/PXEXEC", argumentit_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
