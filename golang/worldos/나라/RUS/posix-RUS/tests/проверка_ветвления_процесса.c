#include <система/ожидание_потомков.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int число_цифр)
{
    (void)писать(STDOUT_FILENO, text, число_цифр);
}

int main(void)
{
    int состояние;
    pid_t parent = получить_номер_процесса();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int дескриптор_файла;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = создать_дочерний_процесс();
    if (child == 0) {
        private_value = 20;
        if (получить_номер_родительского_процесса() != parent || private_value != 20)
            немедленно_завершить(90);
        немедленно_завершить(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        немедленно_завершить(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = ждать_указанного_потомка(child, &состояние, 0);
    if (waited == child && WIFEXITED(состояние) && WEXITSTATUS(состояние) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        немедленно_завершить(1);
    }

    child = создать_дочерний_процесс();
    if (child == 0)
        немедленно_завершить(29);
    waited = ждать_потомка(&состояние);
    if (waited == child && WIFEXITED(состояние) && WEXITSTATUS(состояние) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        немедленно_завершить(1);
    }

    дескриптор_файла = открыть("/USER2", O_RDONLY);
    child = создать_дочерний_процесс();
    if (child == 0) {
        (void)закрыть(дескриптор_файла);
        немедленно_завершить(0);
    }
    waited = ждать_указанного_потомка(child, &состояние, 0);
    if (дескриптор_файла >= 0 && waited == child && читать(дескриптор_файла, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        немедленно_завершить(1);
    }
    (void)закрыть(дескриптор_файла);

    for (iteration = 0; iteration < 2; iteration++) {
        child = создать_дочерний_процесс();
        if (child == 0)
            немедленно_завершить(iteration);
        if (child < 0 || ждать_указанного_потомка(child, &состояние, 0) != child ||
            !WIFEXITED(состояние) || WEXITSTATUS(состояние) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            немедленно_завершить(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    немедленно_завершить(0);
}
