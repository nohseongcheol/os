#include <النظام/انتظار_العمليات_الفرعية.h>
#include <unistd.h>

static void say(const char *text, unsigned int عدد_الخانات)
{
    (void)كتابة(STDOUT_FILENO, text, عدد_الخانات);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)نقل_نهاية_الذاكرة_المتغيرة(0);
    volatile unsigned char *memory;
    pid_t child;
    int الحالة;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)نقل_نهاية_الذاكرة_المتغيرة(32);
    if (start == (void *)-1 || memory != start || نقل_نهاية_الذاكرة_المتغيرة(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        إنهاء_فوري(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        إنهاء_فوري(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (تعيين_نهاية_الذاكرة_المتغيرة((void *)start) != 0 || نقل_نهاية_الذاكرة_المتغيرة(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        إنهاء_فوري(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = إنشاء_عملية_فرعية();
    if (child == 0) {
        if (نقل_نهاية_الذاكرة_المتغيرة(64) != (void *)start)
            إنهاء_فوري(2);
        إنهاء_فوري(0);
    }
    if (child < 0 || انتظار_العملية_الفرعية_المحددة(child, &الحالة, 0) != child ||
        !WIFEXITED(الحالة) || WEXITSTATUS(الحالة) != 0 ||
        نقل_نهاية_الذاكرة_المتغيرة(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        إنهاء_فوري(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    إنهاء_فوري(0);
}
