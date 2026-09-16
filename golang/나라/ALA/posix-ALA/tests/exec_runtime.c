/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int antal_siffror)
{
    (void)Skriv(STDOUT_FILENO, text, antal_siffror);
}

int main(void)
{
    int tillstånd;
    int filbeskrivare;
    char *argument_3[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &tillstånd, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&tillstånd) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    filbeskrivare = Öppna("/USER2", O_RDONLY);
    if (filbeskrivare < 0 || dup2(filbeskrivare, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (filbeskrivare != 10)
        (void)Stäng(filbeskrivare);

    (void)execve("/PXEXEC", argument_3, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
