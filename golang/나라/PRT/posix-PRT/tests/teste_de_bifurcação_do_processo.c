/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sistema/espera_de_filhos.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int número_de_algarismos)
{
    (void)escrever(STDOUT_FILENO, text, número_de_algarismos);
}

int main(void)
{
    int estado;
    pid_t parent = obter_identificador_do_processo();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int descritor_do_ficheiro;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = bifurcar_processo();
    if (child == 0) {
        private_value = 20;
        if (obter_identificador_do_processo_pai() != parent || private_value != 20)
            terminar_imediatamente(90);
        terminar_imediatamente(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        terminar_imediatamente(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = aguardar_filho_indicado(child, &estado, 0);
    if (waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        terminar_imediatamente(1);
    }

    child = bifurcar_processo();
    if (child == 0)
        terminar_imediatamente(29);
    waited = aguardar_filho(&estado);
    if (waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        terminar_imediatamente(1);
    }

    descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    child = bifurcar_processo();
    if (child == 0) {
        (void)fechar(descritor_do_ficheiro);
        terminar_imediatamente(0);
    }
    waited = aguardar_filho_indicado(child, &estado, 0);
    if (descritor_do_ficheiro >= 0 && waited == child && ler(descritor_do_ficheiro, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        terminar_imediatamente(1);
    }
    (void)fechar(descritor_do_ficheiro);

    for (iteration = 0; iteration < 2; iteration++) {
        child = bifurcar_processo();
        if (child == 0)
            terminar_imediatamente(iteration);
        if (child < 0 || aguardar_filho_indicado(child, &estado, 0) != child ||
            !WIFEXITED(estado) || WEXITSTATUS(estado) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            terminar_imediatamente(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    terminar_imediatamente(0);
}
