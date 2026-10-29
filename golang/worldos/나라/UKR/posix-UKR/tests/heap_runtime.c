#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int кількість_цифр)
{
    (void)Запис(STDOUT_FILENO, text, кількість_цифр);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)sbrk(0);
    volatile unsigned char *memory;
    pid_t child;
    int стан;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)sbrk(32);
    if (start == (void *)-1 || memory != start || sbrk(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        _exit(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        _exit(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (brk((void *)start) != 0 || sbrk(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        _exit(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = fork();
    if (child == 0) {
        if (sbrk(64) != (void *)start)
            _exit(2);
        _exit(0);
    }
    if (child < 0 || waitpid(child, &стан, 0) != child ||
        !WIFEXITED(стан) || WEXITSTATUS(стан) != 0 ||
        sbrk(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        _exit(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    _exit(0);
}
