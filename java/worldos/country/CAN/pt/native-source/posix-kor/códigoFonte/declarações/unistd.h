#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int Arquivo_descritor, void *dados, size_t byte_CONT_NÚM);
ssize_t write(int Arquivo_descritor, const void *dados, size_t byte_CONT_NÚM);
int close(int Arquivo_descritor);
off_t lseek(int Arquivo_descritor, off_t DESLOC_VALOR, int ação_raiz);
int dup(int Arquivo_descritor);
int dup2(int Arquivo_descritor, int 새서술자);
int unlink(const char *Arquivo_entrada_nome);
int ftruncate(int Arquivo_descritor, off_t byte_CONT_NÚM);
int fsync(int Arquivo_descritor);
void _exit(int código_de_saída) __attribute__((noreturn));
#endif
