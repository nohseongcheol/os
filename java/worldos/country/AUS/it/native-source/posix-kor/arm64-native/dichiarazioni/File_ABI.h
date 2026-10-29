#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_CONTA_NUMERI_TIPO;
typedef int64_t File_SCARTO_TIPO;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
File_SCARTO_TIPO pk_lseek(int fd, File_SCARTO_TIPO offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, File_SCARTO_TIPO size);
int pk_fsync(int fd);
int pk_size(int fd);
int aperto_File(const char *percorso, int metodo_MODA, ...);
입출력결과형 파일자료읽기(int file, void *dati, size_t articolo_CONTA_NUMERI);
입출력결과형 scrivere_File_dati(int file, const void *dati, size_t articolo_CONTA_NUMERI);
int Chiudi_File(int file);
File_SCARTO_TIPO cercare_File(int file, File_SCARTO_TIPO 거리, int azione_radice);
int rimuovere_File_voce_nome(const char *percorso);
int set_File_durata(int file, File_SCARTO_TIPO Dimensione);
int commit_File(int file);
int dimensioni_del_file(int file);
#ifdef __cplusplus
}
#endif
#define numero_errore (*pk_errno_location())
#define di_sola_lettura_VALORE 0
#define sola_scrittura_VALORE 1
#define in_lettura_scrittura 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define tagliare_Sommario 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define Regolari_radice 1
#define chiudere_origine 2
#endif
