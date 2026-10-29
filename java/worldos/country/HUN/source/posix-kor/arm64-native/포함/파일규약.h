#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bájt_DARAB_beír;
typedef int64_t Fájl_Ofszet_beír;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fájl_Ofszet_beír pk_lseek(int fd, Fájl_Ofszet_beír offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fájl_Ofszet_beír size);
int pk_fsync(int fd);
int pk_size(int fd);
int készít_Fájl(const char *ÚTVONAL, int metódus_mód, ...);
입출력결과형 파일자료읽기(int Fájl, void *adat, size_t cikk_DARAB);
입출력결과형 ír_Fájl_adat(int Fájl, const void *adat, size_t cikk_DARAB);
int bezár_Fájl(int Fájl);
Fájl_Ofszet_beír keres_Fájl(int Fájl, Fájl_Ofszet_beír 거리, int teendő_gyök);
int eltávolít_Fájl_bejegyzés_név(const char *ÚTVONAL);
int halmaz_Fájl_hossz(int Fájl, Fájl_Ofszet_beír Méret);
int véglegesít_Files(int Fájl);
int fájlméret(int Fájl);
#ifdef __cplusplus
}
#endif
#define hibaszám (*pk_errno_location())
#define írásvédett_ÉRTÉK 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define vág_Tartalom 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define aktuális_gyök 1
#define megszüntet_eredet 2
#endif
