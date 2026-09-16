#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/identidade_do_sistema.h>
#include <sistema/espera_de_filhos.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct estado_do_ficheiro st;
    struct utsname identidade_do_sistema;
    int descritor_do_ficheiro = abrir("/USER1", O_RDONLY);
    int copy = descritor_do_ficheiro >= 0 ? duplicar_referência_de_ficheiro_aberto(descritor_do_ficheiro) : -1;
    if (copy >= 0) fechar(copy);
    if (descritor_do_ficheiro >= 0) {
        obter_estado_do_ficheiro_aberto(descritor_do_ficheiro, &st);
        mover_posição_do_ficheiro(descritor_do_ficheiro, 0, SEEK_SET);
        fechar(descritor_do_ficheiro);
    }
    estado_do_ficheiro("/", &st);
    obter_informações_do_sistema(&identidade_do_sistema);
    obter_caminho_do_diretório_de_trabalho(cwd, sizeof(cwd));
    return errno + obter_identificador_do_processo() + obter_identificador_do_processo_pai();
}
