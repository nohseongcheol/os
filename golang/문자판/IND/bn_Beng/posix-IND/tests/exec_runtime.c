/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int অঙ্কের_সংখ্যা)
{
    (void)লেখা(STDOUT_FILENO, text, অঙ্কের_সংখ্যা);
}

int main(void)
{
    int অবস্থা;
    int নথি_নির্দেশক;
    char *আর্গুমেন্ট_তালিকা_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (waitpid(-1, &অবস্থা, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (wait(&অবস্থা) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    নথি_নির্দেশক = open("/USER2", O_RDONLY);
    if (নথি_নির্দেশক < 0 || dup2(নথি_নির্দেশক, 10) != 10 || fcntl(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        _exit(98);
    }
    if (নথি_নির্দেশক != 10)
        (void)close(নথি_নির্দেশক);

    (void)execve("/PXEXEC", আর্গুমেন্ট_তালিকা_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    _exit(99);
}
