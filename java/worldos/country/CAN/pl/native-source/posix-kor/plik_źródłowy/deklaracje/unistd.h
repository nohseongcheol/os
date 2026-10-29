#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int Plik_deskryptor, void *dane, size_t bajt_ILE_LICZB);
ssize_t write(int Plik_deskryptor, const void *dane, size_t bajt_ILE_LICZB);
int close(int Plik_deskryptor);
off_t lseek(int Plik_deskryptor, off_t przesunąć_WARTOŚĆ_450fc799, int Project_korzeń);
int dup(int Plik_deskryptor);
int dup2(int Plik_deskryptor, int 새서술자);
int unlink(const char *Plik_wpis_nazwa);
int ftruncate(int Plik_deskryptor, off_t bajt_ILE_LICZB);
int fsync(int Plik_deskryptor);
void _exit(int kod_zakończenia) __attribute__((noreturn));
#endif
