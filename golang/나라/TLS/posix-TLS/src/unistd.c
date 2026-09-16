/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sistema/stat.h>
#include <sistema/espera_de_filhos.h>
#include <unistd.h>
#include <sistema/syscall.h>

enum {
    SYS_terminar_imediatamente = 1,
    SYS_bifurcar_processo = 2,
    SYS_ler = 3,
    SYS_escrever = 4,
    SYS_fechar = 6,
    SYS_substituir_programa_em_execução = 11,
    SYS_mudar_diretório_de_trabalho = 12,
    SYS_mover_posição_do_ficheiro = 19,
    SYS_obter_identificador_do_processo = 20,
    SYS_obter_identificador_do_utilizador = 24,
    SYS_verificar_permissões_de_acesso = 33,
    SYS_sincronizar_todos_os_dados = 36,
    SYS_duplicar_referência_de_ficheiro_aberto = 41,
    SYS_definir_fim_da_memória_dinâmica = 45,
    SYS_obter_identificador_do_grupo = 47,
    SYS_obter_identificador_efetivo_do_utilizador = 49,
    SYS_obter_identificador_efetivo_do_grupo = 50,
    SYS_duplicar_referência_para_número_indicado = 63,
    SYS_obter_identificador_do_processo_pai = 64,
    SYS_sincronizar_dados_do_ficheiro = 118,
    SYS_obter_caminho_do_diretório_de_trabalho = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void terminar_imediatamente(int estado)
{
    SC1(SYS_terminar_imediatamente, estado);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t ler(int descritor_do_ficheiro, void *memória_intermédia_de_transferência, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_ler, descritor_do_ficheiro, memória_intermédia_de_transferência, count));
}

ssize_t escrever(int descritor_do_ficheiro, const void *memória_intermédia_de_transferência, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_escrever, descritor_do_ficheiro, memória_intermédia_de_transferência, count));
}

int fechar(int descritor_do_ficheiro)
{
    return (int)__syscall_result(SC1(SYS_fechar, descritor_do_ficheiro));
}

off_t mover_posição_do_ficheiro(int descritor_do_ficheiro, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_mover_posição_do_ficheiro, descritor_do_ficheiro, offset, whence));
}

pid_t bifurcar_processo(void)
{
    return (pid_t)__syscall_result(SC0(SYS_bifurcar_processo));
}

int substituir_programa_em_execução(const char *caminho, char *const argumentos_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_substituir_programa_em_execução, caminho, argumentos_2, envp));
}

pid_t obter_identificador_do_processo(void) { return (pid_t)SC0(SYS_obter_identificador_do_processo); }
pid_t obter_identificador_do_processo_pai(void) { return (pid_t)SC0(SYS_obter_identificador_do_processo_pai); }
uid_t obter_identificador_do_utilizador(void) { return (uid_t)SC0(SYS_obter_identificador_do_utilizador); }
uid_t obter_identificador_efetivo_do_utilizador(void) { return (uid_t)SC0(SYS_obter_identificador_efetivo_do_utilizador); }
gid_t obter_identificador_do_grupo(void) { return (gid_t)SC0(SYS_obter_identificador_do_grupo); }
gid_t obter_identificador_efetivo_do_grupo(void) { return (gid_t)SC0(SYS_obter_identificador_efetivo_do_grupo); }

int verificar_permissões_de_acesso(const char *caminho, int mode)
{
    return (int)__syscall_result(SC2(SYS_verificar_permissões_de_acesso, caminho, mode));
}

int mudar_diretório_de_trabalho(const char *caminho)
{
    return (int)__syscall_result(SC1(SYS_mudar_diretório_de_trabalho, caminho));
}

char *obter_caminho_do_diretório_de_trabalho(char *memória_intermédia_de_transferência, size_t número_de_algarismos)
{
    long result = __syscall_result(SC2(SYS_obter_caminho_do_diretório_de_trabalho, memória_intermédia_de_transferência, número_de_algarismos));
    return result < 0 ? (char *)0 : memória_intermédia_de_transferência;
}

int duplicar_referência_de_ficheiro_aberto(int descritor_do_ficheiro)
{
    return (int)__syscall_result(SC1(SYS_duplicar_referência_de_ficheiro_aberto, descritor_do_ficheiro));
}

int duplicar_referência_para_número_indicado(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_duplicar_referência_para_número_indicado, oldfd, newfd));
}

int sincronizar_dados_do_ficheiro(int descritor_do_ficheiro)
{
    return (int)__syscall_result(SC1(SYS_sincronizar_dados_do_ficheiro, descritor_do_ficheiro));
}

void sincronizar_todos_os_dados(void)
{
    SC0(SYS_sincronizar_todos_os_dados);
}

int verificar_se_é_terminal(int descritor_do_ficheiro)
{
    struct estado_do_ficheiro st;
    if (obter_estado_do_ficheiro_aberto(descritor_do_ficheiro, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int definir_fim_da_memória_dinâmica(void *address)
{
    long result = SC1(SYS_definir_fim_da_memória_dinâmica, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *mover_fim_da_memória_dinâmica(int increment)
{
    long current = SC1(SYS_definir_fim_da_memória_dinâmica, 0);
    long requested = current + increment;
    if (increment != 0 && definir_fim_da_memória_dinâmica((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t aguardar_filho_indicado(pid_t pid, int *estado, int options)
{
    long result;
    do {
        result = SC3(7, pid, estado, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t aguardar_filho(int *estado)
{
    return aguardar_filho_indicado(-1, estado, 0);
}
