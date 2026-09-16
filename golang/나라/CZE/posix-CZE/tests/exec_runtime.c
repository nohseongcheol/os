/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int počet_číslic)
{
    (void)Zápis(STDOUT_FILENO, text, počet_číslic);
}

int main(void)
{
    int stav;
    int deskriptor_souboru;
    char *argumenty_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &stav, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&stav) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    deskriptor_souboru = Otevřít("/USER2", O_RDONLY);
    if (deskriptor_souboru < 0 || dup2(deskriptor_souboru, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (deskriptor_souboru != 10)
        (void)Zavřít(deskriptor_souboru);

    (void)execve("/PXEXEC", argumenty_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
