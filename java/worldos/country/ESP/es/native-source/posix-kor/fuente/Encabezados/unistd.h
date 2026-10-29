#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int descriptorArchivo, void *Datos, size_t númeroElementosByte);
ssize_t write(int descriptorArchivo, const void *Datos, size_t númeroElementosByte);
int close(int descriptorArchivo);
off_t lseek(int descriptorArchivo, off_t valorDesfase, int raízProyecto);
int dup(int descriptorArchivo);
int dup2(int descriptorArchivo, int descriptorNuevo);
int unlink(const char *nombreEntradaElementoArchivo);
int ftruncate(int descriptorArchivo, off_t númeroElementosByte);
int fsync(int descriptorArchivo);
void _exit(int códigoSalir) __attribute__((noreturn));
#endif
