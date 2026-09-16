#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sistema/stat.h>
int __posix_library_test(void);

int main(void)
{
    char memória_intermédia_de_transferência_2[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int descritor_do_ficheiro = abrir("/USER2", O_RDONLY);
    struct estado_do_ficheiro st;
    if (descritor_do_ficheiro < 0 || obter_estado_do_ficheiro_aberto(descritor_do_ficheiro, &st) < 0 || ler(descritor_do_ficheiro, memória_intermédia_de_transferência_2, 4) != 4 ||
        (unsigned char)memória_intermédia_de_transferência_2[0] != 0x7f || memória_intermédia_de_transferência_2[1] != 'E' || memória_intermédia_de_transferência_2[2] != 'L' || memória_intermédia_de_transferência_2[3] != 'F' ||
        mover_posição_do_ficheiro(descritor_do_ficheiro, 0, SEEK_SET) != 0 || fechar(descritor_do_ficheiro) < 0 || obter_identificador_do_processo() <= 0)
        goto failure;
    errno = 0;
    if (ler(-1, memória_intermédia_de_transferência_2, 1) != -1 || errno != EBADF)
        goto failure;
    if (__posix_library_test() != 0)
        goto failure;
    if (escrever(STDOUT_FILENO, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto failure;
    return 0;
failure:
    escrever(STDOUT_FILENO, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
