#include <errno.h>
#include <fcntl.h>
#include <sistema/espera_de_filhos.h>
#include <unistd.h>

static void say(const char *text, unsigned int número_de_algarismos)
{
    (void)escrever(STDOUT_FILENO, text, número_de_algarismos);
}

int main(void)
{
    int estado;
    int descritor_do_ficheiro;
    char *argumentos_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (aguardar_filho_indicado(-1, &estado, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (aguardar_filho(&estado) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    if (descritor_do_ficheiro < 0 || duplicar_referência_para_número_indicado(descritor_do_ficheiro, 10) != 10 || controlar_ficheiro(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        terminar_imediatamente(98);
    }
    if (descritor_do_ficheiro != 10)
        (void)fechar(descritor_do_ficheiro);

    (void)substituir_programa_em_execução("/PXEXEC", argumentos_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    terminar_imediatamente(99);
}
