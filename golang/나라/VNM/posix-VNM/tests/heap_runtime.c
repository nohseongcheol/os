/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/wait.h>
#include <unistd.h>

static void say(const char *text, unsigned int số_chữ_số)
{
    (void)Ghi(STDOUT_FILENO, text, số_chữ_số);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)sbrk(0);
    volatile unsigned char *memory;
    pid_t child;
    int trạng_thái;

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
    if (child < 0 || waitpid(child, &trạng_thái, 0) != child ||
        !WIFEXITED(trạng_thái) || WEXITSTATUS(trạng_thái) != 0 ||
        sbrk(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        _exit(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    _exit(0);
}
