#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int File_descrittore, void *dati, size_t byte_CONTA_NUMERI);
ssize_t write(int File_descrittore, const void *dati, size_t byte_CONTA_NUMERI);
int close(int File_descrittore);
off_t lseek(int File_descrittore, off_t SCARTO_VALORE, int azione_radice);
int dup(int File_descrittore);
int dup2(int File_descrittore, int 새서술자);
int unlink(const char *File_voce_nome);
int ftruncate(int File_descrittore, off_t byte_CONTA_NUMERI);
int fsync(int File_descrittore);
void _exit(int codice_di_uscita) __attribute__((noreturn));
#endif
