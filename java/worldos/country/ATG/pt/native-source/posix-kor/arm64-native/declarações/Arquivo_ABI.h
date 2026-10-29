#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_CONT_NÚM_TIPO;
typedef int64_t Arquivo_DESLOC_TIPO;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Arquivo_DESLOC_TIPO pk_lseek(int fd, Arquivo_DESLOC_TIPO offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Arquivo_DESLOC_TIPO size);
int pk_fsync(int fd);
int pk_size(int fd);
int abrir_Arquivo(const char *caminho, int método_MODO, ...);
입출력결과형 leitura_Arquivo_dados(int ficheiro, void *dados, size_t item_CONT_NÚM);
입출력결과형 gravar_Arquivo_dados(int ficheiro, const void *dados, size_t item_CONT_NÚM);
int Close_Arquivo(int ficheiro);
Arquivo_DESLOC_TIPO busca_Arquivo(int ficheiro, Arquivo_DESLOC_TIPO 거리, int ação_raiz);
int remover_Arquivo_entrada_nome(const char *caminho);
int set_Arquivo_duração(int ficheiro, Arquivo_DESLOC_TIPO Tamanho);
int commit_Arquivos(int ficheiro);
int tamanho_do_arquivo(int ficheiro);
#ifdef __cplusplus
}
#endif
#define número_do_erro (*pk_errno_location())
#define somente_leitura_VALOR 0
#define somente_gravação_VALOR 1
#define de_leitura_gravação 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define cortar_Sumário 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define em_dia_raiz 1
#define encerrar_origem 2
#endif
