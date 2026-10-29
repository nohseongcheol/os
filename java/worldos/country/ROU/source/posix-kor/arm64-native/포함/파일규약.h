#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_COUNT_Tip;
typedef int64_t Fișier_OFFSET_Tip;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fișier_OFFSET_Tip pk_lseek(int fd, Fișier_OFFSET_Tip offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fișier_OFFSET_Tip size);
int pk_fsync(int fd);
int pk_size(int fd);
int crea_Fișier(const char *Cale, int metodă_mod, ...);
입출력결과형 파일자료읽기(int Fișier, void *date, size_t element_COUNT);
입출력결과형 scriere_Fișier_date(int Fișier, const void *date, size_t element_COUNT);
int închide_Fișier(int Fișier);
Fișier_OFFSET_Tip căuta_Fișier(int Fișier, Fișier_OFFSET_Tip 거리, int Project_rădăcină);
int elimina_Fișier_intrare_nume(const char *Cale);
int set_Fișier_lungime(int Fișier, Fișier_OFFSET_Tip Mărime);
int comitere_Fișiere(int Fișier);
int dimensiune_fișier(int Fișier);
#ifdef __cplusplus
}
#endif
#define număr_de_eroare (*pk_errno_location())
#define doar_în_citire_VALUE 0
#define 쓰기전용 1
#define citire_scriere 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define trunchia_TOC 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define curent_rădăcină 1
#define 끝기준 2
#endif
