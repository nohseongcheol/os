#include <система/ожидание_потомков.h>
#include <unistd.h>

static void say(const char *text, unsigned int число_цифр)
{
    (void)писать(STDOUT_FILENO, text, число_цифр);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)сместить_конец_динамической_памяти(0);
    volatile unsigned char *memory;
    pid_t child;
    int состояние;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)сместить_конец_динамической_памяти(32);
    if (start == (void *)-1 || memory != start || сместить_конец_динамической_памяти(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        немедленно_завершить(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        немедленно_завершить(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (задать_конец_динамической_памяти((void *)start) != 0 || сместить_конец_динамической_памяти(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        немедленно_завершить(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = создать_дочерний_процесс();
    if (child == 0) {
        if (сместить_конец_динамической_памяти(64) != (void *)start)
            немедленно_завершить(2);
        немедленно_завершить(0);
    }
    if (child < 0 || ждать_указанного_потомка(child, &состояние, 0) != child ||
        !WIFEXITED(состояние) || WEXITSTATUS(состояние) != 0 ||
        сместить_конец_динамической_памяти(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        немедленно_завершить(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    немедленно_завершить(0);
}
