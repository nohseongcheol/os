/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <système/attente_des_enfants.h>
#include <unistd.h>

static void say(const char *text, unsigned int nombre_de_chiffres)
{
    (void)écrire(STDOUT_FILENO, text, nombre_de_chiffres);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)déplacer_la_fin_de_mémoire_dynamique(0);
    volatile unsigned char *memory;
    pid_t child;
    int état;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)déplacer_la_fin_de_mémoire_dynamique(32);
    if (start == (void *)-1 || memory != start || déplacer_la_fin_de_mémoire_dynamique(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        terminer_immédiatement(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        terminer_immédiatement(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (fixer_la_fin_de_mémoire_dynamique((void *)start) != 0 || déplacer_la_fin_de_mémoire_dynamique(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        terminer_immédiatement(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = dédoubler_le_processus();
    if (child == 0) {
        if (déplacer_la_fin_de_mémoire_dynamique(64) != (void *)start)
            terminer_immédiatement(2);
        terminer_immédiatement(0);
    }
    if (child < 0 || attendre_un_enfant_désigné(child, &état, 0) != child ||
        !WIFEXITED(état) || WEXITSTATUS(état) != 0 ||
        déplacer_la_fin_de_mémoire_dynamique(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        terminer_immédiatement(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    terminer_immédiatement(0);
}
