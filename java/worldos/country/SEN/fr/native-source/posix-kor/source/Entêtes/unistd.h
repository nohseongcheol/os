#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int descripteurFichier, void *Données, size_t nombreÉlémentsOctet);
ssize_t write(int descripteurFichier, const void *Données, size_t nombreÉlémentsOctet);
int close(int descripteurFichier);
off_t lseek(int descripteurFichier, off_t valeurDécalage, int racineProjet);
int dup(int descripteurFichier);
int dup2(int descripteurFichier, int descripteurNouveau);
int unlink(const char *nomEntréeÉlémentFichier);
int ftruncate(int descripteurFichier, off_t nombreÉlémentsOctet);
int fsync(int descripteurFichier);
void _exit(int codeQuitter) __attribute__((noreturn));
#endif
