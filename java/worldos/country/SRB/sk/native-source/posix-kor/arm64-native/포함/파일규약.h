#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t Byte_COUNT_Typ;
typedef int64_t Súbor_Posun_Typ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Súbor_Posun_Typ pk_lseek(int fd, Súbor_Posun_Typ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Súbor_Posun_Typ size);
int pk_fsync(int fd);
int pk_size(int fd);
int otvoriť_Súbor(const char *Cesta, int metóda_MODE, ...);
입출력결과형 파일자료읽기(int Súbor, void *údaje, size_t položka_COUNT);
입출력결과형 zapísať_Súbor_údaje(int Súbor, const void *údaje, size_t položka_COUNT);
int Zavrieť_Súbor(int Súbor);
Súbor_Posun_Typ hľadať_Súbor(int Súbor, Súbor_Posun_Typ 거리, int akcia_koreň);
int odobrať_Súbor_položka_názov(const char *Cesta);
int množina_Súbor_dĺžka(int Súbor, Súbor_Posun_Typ Veľkosť);
int potvrdenie_ukladací_priestor_súborov(int Súbor);
int veľkosť_súboru(int Súbor);
#ifdef __cplusplus
}
#endif
#define chybové_číslo (*pk_errno_location())
#define iba_na_čítanie_VALUE 0
#define 쓰기전용 1
#define na_čítanie_a_zapisovanie 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define skrátiť_Obsah 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define v_termíne_splatnosti_koreň 1
#define 끝기준 2
#endif
