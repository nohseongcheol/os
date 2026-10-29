#include <System/Kindwartung.h>
#include <unistd.h>

static void say(const char *text, unsigned int Ziffernanzahl)
{
    (void)schreiben(STDOUT_FILENO, text, Ziffernanzahl);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)Speicherende_verschieben(0);
    volatile unsigned char *memory;
    pid_t child;
    int Status;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)Speicherende_verschieben(32);
    if (start == (void *)-1 || memory != start || Speicherende_verschieben(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        sofort_beenden(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        sofort_beenden(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (Speicherende_setzen((void *)start) != 0 || Speicherende_verschieben(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        sofort_beenden(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = Prozess_verzweigen();
    if (child == 0) {
        if (Speicherende_verschieben(64) != (void *)start)
            sofort_beenden(2);
        sofort_beenden(0);
    }
    if (child < 0 || bestimmtes_Kind_abwarten(child, &Status, 0) != child ||
        !WIFEXITED(Status) || WEXITSTATUS(Status) != 0 ||
        Speicherende_verschieben(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        sofort_beenden(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    sofort_beenden(0);
}
