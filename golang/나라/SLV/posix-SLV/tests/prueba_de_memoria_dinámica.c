/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sistema/espera_de_hijos.h>
#include <unistd.h>

static void say(const char *text, unsigned int cantidad_de_dígitos)
{
    (void)escribir(STDOUT_FILENO, text, cantidad_de_dígitos);
}

int main(void)
{
    volatile unsigned char *start = (volatile unsigned char *)mover_fin_de_memoria_dinámica(0);
    volatile unsigned char *memory;
    pid_t child;
    int estado;

    say("\nPOSIX-HEAP:START\n", 18);
    memory = (volatile unsigned char *)mover_fin_de_memoria_dinámica(32);
    if (start == (void *)-1 || memory != start || mover_fin_de_memoria_dinámica(0) != (void *)(start + 32)) {
        say("PTEST:FAIL:sbrk-grow\n", 22);
        terminar_inmediatamente(1);
    }
    say("PTEST:PASS:sbrk-grow\n", 22);
    memory[0] = 0x5a;
    memory[31] = 0xa5;
    if (memory[0] != 0x5a || memory[31] != 0xa5) {
        say("PTEST:FAIL:sbrk-memory\n", 24);
        terminar_inmediatamente(1);
    }
    say("PTEST:PASS:sbrk-memory\n", 24);
    if (fijar_fin_de_memoria_dinámica((void *)start) != 0 || mover_fin_de_memoria_dinámica(0) != (void *)start) {
        say("PTEST:FAIL:brk-restore\n", 24);
        terminar_inmediatamente(1);
    }
    say("PTEST:PASS:brk-restore\n", 24);

    child = bifurcar_proceso();
    if (child == 0) {
        if (mover_fin_de_memoria_dinámica(64) != (void *)start)
            terminar_inmediatamente(2);
        terminar_inmediatamente(0);
    }
    if (child < 0 || esperar_hijo_indicado(child, &estado, 0) != child ||
        !WIFEXITED(estado) || WEXITSTATUS(estado) != 0 ||
        mover_fin_de_memoria_dinámica(0) != (void *)start) {
        say("PTEST:FAIL:brk-process-isolation\n", 33);
        terminar_inmediatamente(1);
    }
    say("PTEST:PASS:brk-process-isolation\n", 33);
    say("POSIX-HEAP:PASS\n", 16);
    terminar_inmediatamente(0);
}
