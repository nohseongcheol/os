#include <sistema/espera_de_filhos.h>
#include <unistd.h>

static void say(const char *text, unsigned int número_de_algarismos)
{
    (void)escrever(STDOUT_FILENO, text, número_de_algarismos);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)mover_fim_da_memória_dinâmica(0);
    volatile unsigned char *memory;
    pid_t child;
    int estado;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)mover_fim_da_memória_dinâmica(32);
    if (start == (void *)-1 || memory != start || mover_fim_da_memória_dinâmica(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        terminar_imediatamente(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        terminar_imediatamente(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (definir_fim_da_memória_dinâmica((void *)start) != 0 || mover_fim_da_memória_dinâmica(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        terminar_imediatamente(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = bifurcar_processo();
    if (child == 0) {
        if (mover_fim_da_memória_dinâmica(64) != (void *)start)
            terminar_imediatamente(2);
        terminar_imediatamente(0);
    }
    if (child < 0 || aguardar_filho_indicado(child, &estado, 0) != child ||
        !WIFEXITED(estado) || WEXITSTATUS(estado) != 0 ||
        mover_fim_da_memória_dinâmica(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        terminar_imediatamente(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    terminar_imediatamente(0);
}
