#include <errno.h>
#include <fcntl.h>
#include <sistema/espera_de_hijos.h>
#include <unistd.h>

static void say(const char *text, unsigned int cantidad_de_dígitos)
{
    (void)escribir(STDOUT_FILENO, text, cantidad_de_dígitos);
}

int main(void)
{
    int estado;
    int descriptor_del_archivo;
    char *argumentos_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (esperar_hijo_indicado(-1, &estado, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (esperar_hijo(&estado) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    descriptor_del_archivo = abrir("/USER2", O_RDONLY);
    if (descriptor_del_archivo < 0 || duplicar_referencia_al_número_indicado(descriptor_del_archivo, 10) != 10 || controlar_archivo(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        terminar_inmediatamente(98);
    }
    if (descriptor_del_archivo != 10)
        (void)cerrar(descriptor_del_archivo);

    (void)sustituir_programa_en_ejecución("/PXEXEC", argumentos_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    terminar_inmediatamente(99);
}
