#include <sys/wait.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int antal_siffror)
{
    (void)Skriv(STDOUT_FILENO, text, antal_siffror);
}

int main(void)
{
    int tillstånd;
    pid_t parent = getpid();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int filbeskrivare;
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
    waited = waitpid(child, &tillstånd, 0);
    if (waited == child && WIFEXITED(tillstånd) && WEXITSTATUS(tillstånd) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        _exit(1);
    }

    child = fork();
    if (child == 0)
        _exit(29);
    waited = wait(&tillstånd);
    if (waited == child && WIFEXITED(tillstånd) && WEXITSTATUS(tillstånd) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        _exit(1);
    }

    filbeskrivare = Öppna("/USER2", O_RDONLY);
    child = fork();
    if (child == 0) {
        (void)Stäng(filbeskrivare);
        _exit(0);
    }
    waited = waitpid(child, &tillstånd, 0);
    if (filbeskrivare >= 0 && waited == child && Läs(filbeskrivare, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        _exit(1);
    }
    (void)Stäng(filbeskrivare);

    for (iteration = 0; iteration < 2; iteration++) {
        child = fork();
        if (child == 0)
            _exit(iteration);
        if (child < 0 || waitpid(child, &tillstånd, 0) != child ||
            !WIFEXITED(tillstånd) || WEXITSTATUS(tillstånd) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            _exit(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    _exit(0);
}
