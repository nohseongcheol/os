#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <definições_básicas.h>
#include <sistema/tipos_de_dados.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void terminar_imediatamente(int estado) __attribute__((noreturn));
ssize_t ler(int descritor_do_ficheiro, void *memória_intermédia_de_transferência, size_t count);
ssize_t escrever(int descritor_do_ficheiro, const void *memória_intermédia_de_transferência, size_t count);
int fechar(int descritor_do_ficheiro);
off_t mover_posição_do_ficheiro(int descritor_do_ficheiro, off_t offset, int whence);
pid_t bifurcar_processo(void);
int substituir_programa_em_execução(const char *caminho, char *const argumentos_2[], char *const envp[]);
pid_t obter_identificador_do_processo(void);
pid_t obter_identificador_do_processo_pai(void);
uid_t obter_identificador_do_utilizador(void);
uid_t obter_identificador_efetivo_do_utilizador(void);
gid_t obter_identificador_do_grupo(void);
gid_t obter_identificador_efetivo_do_grupo(void);
int verificar_permissões_de_acesso(const char *caminho, int mode);
int mudar_diretório_de_trabalho(const char *caminho);
char *obter_caminho_do_diretório_de_trabalho(char *memória_intermédia_de_transferência, size_t número_de_algarismos);
int duplicar_referência_de_ficheiro_aberto(int descritor_do_ficheiro);
int duplicar_referência_para_número_indicado(int oldfd, int newfd);
int sincronizar_dados_do_ficheiro(int descritor_do_ficheiro);
void sincronizar_todos_os_dados(void);
int verificar_se_é_terminal(int descritor_do_ficheiro);
int definir_fim_da_memória_dinâmica(void *address);
void *mover_fim_da_memória_dinâmica(int increment);
#ifdef __cplusplus
}
#endif

#endif
