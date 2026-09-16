/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int кількість_цифр)
{
    (void)Запис(STDOUT_FILENO, text, кількість_цифр);
}

int main(void)
{
    int стан;
    pid_t parent = getpid();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int дескриптор_файла;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = fork();
    if (child == 0) {
        private_value = 20;
        if (getppid() != parent || private_value != 20)
            _exit(90);
        _exit(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        _exit(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = waitpid(child, &стан, 0);
    if (waited == child && WIFEXITED(стан) && WEXITSTATUS(стан) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        _exit(1);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    waited = wait(&стан);
    if (waited == child && WIFEXITED(стан) && WEXITSTATUS(стан) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        _exit(1);
    }

    дескриптор_файла = Відкрити("/USER2", O_RDONLY);
    child = fork();
    if (child == 0) {
        (void)Закрити(дескриптор_файла);
        _exit(0);
    }
    waited = waitpid(child, &стан, 0);
    if (дескриптор_файла >= 0 && waited == child && Читання(дескриптор_файла, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        _exit(1);
    }
    (void)Закрити(дескриптор_файла);

    for (iteration = 0; iteration < 2; iteration++) {
        child = fork();
        if (child == 0)
            _exit(iteration);
        if (child < 0 || waitpid(child, &стан, 0) != child ||
            !WIFEXITED(стан) || WEXITSTATUS(стан) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            _exit(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    _exit(0);
}
