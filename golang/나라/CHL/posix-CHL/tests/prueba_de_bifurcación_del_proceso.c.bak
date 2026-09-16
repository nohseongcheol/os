#include <sistema/espera_de_hijos.h>
#include <fcntl.h>
#include <unistd.h>

static void say(const char *text, unsigned int cantidad_de_dígitos)
{
    (void)escribir(STDOUT_FILENO, text, cantidad_de_dígitos);
}

int main(void)
{
    int estado;
    pid_t parent = obtener_identificador_de_proceso();
    pid_t child;
    pid_t waited;
    volatile int private_value = 10;
    int descriptor_del_archivo;
    char byte;
    int iteration;

    say("\nPOSIX-FORK:START\n", 18);
    child = bifurcar_proceso();
    if (child == 0) {
        private_value = 20;
        if (obtener_identificador_del_padre() != parent || private_value != 20)
            terminar_inmediatamente(90);
        terminar_inmediatamente(23);
    }
    if (child < 0) {
        say("PTEST:FAIL:fork-return\n", 23);
        terminar_inmediatamente(1);
    }
    say("PTEST:PASS:fork-return\n", 23);
    waited = esperar_hijo_indicado(child, &estado, 0);
    if (waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 23 &&
        private_value == 10) {
        say("PTEST:PASS:fork-wait-exit\n", 26);
    } else {
        say("PTEST:FAIL:fork-wait-exit\n", 26);
        terminar_inmediatamente(1);
    }

    child = bifurcar_proceso();
    if (child == 0)
        terminar_inmediatamente(29);
    waited = esperar_hijo(&estado);
    if (waited == child && WIFEXITED(estado) && WEXITSTATUS(estado) == 29)
        say("PTEST:PASS:blocking-wait\n", 25);
    else {
        say("PTEST:FAIL:blocking-wait\n", 25);
        terminar_inmediatamente(1);
    }

    descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    child = bifurcar_proceso();
    if (child == 0) {
        (void)cerrar(descriptor_del_archivo);
        terminar_inmediatamente(0);
    }
    waited = esperar_hijo_indicado(child, &estado, 0);
    if (descriptor_del_archivo >= 0 && waited == child && leer(descriptor_del_archivo, &byte, 1) == 1 &&
        (unsigned char)byte == 0x7f)
        say("PTEST:PASS:fork-fd-isolation\n", 29);
    else {
        say("PTEST:FAIL:fork-fd-isolation\n", 29);
        terminar_inmediatamente(1);
    }
    (void)cerrar(descriptor_del_archivo);

    for (iteration = 0; iteration < 2; iteration++) {
        child = bifurcar_proceso();
        if (child == 0)
            terminar_inmediatamente(iteration);
        if (child < 0 || esperar_hijo_indicado(child, &estado, 0) != child ||
            !WIFEXITED(estado) || WEXITSTATUS(estado) != iteration) {
            say("PTEST:FAIL:fork-stress\n", 23);
            terminar_inmediatamente(1);
        }
    }
    say("PTEST:PASS:fork-stress\n", 23);
    say("POSIX-FORK:PASS\n", 16);
    terminar_inmediatamente(0);
}
