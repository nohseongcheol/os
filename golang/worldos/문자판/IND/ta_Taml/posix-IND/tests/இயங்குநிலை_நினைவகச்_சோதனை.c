#include <அமைப்பு/சேய்_காத்திருப்பு.h>
#include <unistd.h>

static void say(const char *text, unsigned int இலக்கங்களின்_எண்ணிக்கை)
{
    (void)எழுது(STDOUT_FILENO, text, இலக்கங்களின்_எண்ணிக்கை);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)மாறும்_நினைவக_முடிவை_நகர்த்து(0);
    volatile unsigned char *memory;
    pid_t child;
    int நிலை;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)மாறும்_நினைவக_முடிவை_நகர்த்து(32);
    if (start == (void *)-1 || memory != start || மாறும்_நினைவக_முடிவை_நகர்த்து(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        உடனே_முடி(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        உடனே_முடி(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (மாறும்_நினைவக_முடிவை_அமை((void *)start) != 0 || மாறும்_நினைவக_முடிவை_நகர்த்து(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        உடனே_முடி(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = சேய்_செயல்முறையை_உருவாக்கு();
    if (child == 0) {
        if (மாறும்_நினைவக_முடிவை_நகர்த்து(64) != (void *)start)
            உடனே_முடி(2);
        உடனே_முடி(0);
    }
    if (child < 0 || குறித்த_சேய்க்குக்_காத்திரு(child, &நிலை, 0) != child ||
        !WIFEXITED(நிலை) || WEXITSTATUS(நிலை) != 0 ||
        மாறும்_நினைவக_முடிவை_நகர்த்து(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        உடனே_முடி(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    உடனே_முடி(0);
}
