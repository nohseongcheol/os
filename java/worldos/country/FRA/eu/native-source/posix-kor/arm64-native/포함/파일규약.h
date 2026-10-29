#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_ZENBATU_MOTA;
typedef int64_t fitxategi_Geruzak_MOTA;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fitxategi_Geruzak_MOTA pk_lseek(int fd, fitxategi_Geruzak_MOTA offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fitxategi_Geruzak_MOTA size);
int pk_fsync(int fd);
int pk_size(int fd);
int ireki_fitxategi(const char *Bide_izena, int 방식, ...);
입출력결과형 파일자료읽기(int Fitxategia, void *datuak, size_t elementu_ZENBATU);
입출력결과형 idatzi_fitxategi_datuak(int Fitxategia, const void *datuak, size_t elementu_ZENBATU);
int itxi_fitxategi(int Fitxategia);
fitxategi_Geruzak_MOTA bilatu_fitxategi(int Fitxategia, fitxategi_Geruzak_MOTA 거리, int Project_erro);
int kendu_fitxategi_sarrera_izen(const char *Bide_izena);
int sorta_fitxategi_luzera(int Fitxategia, fitxategi_Geruzak_MOTA Tamaina);
int 파일저장확정(int Fitxategia);
int 파일크기(int Fitxategia);
#ifdef __cplusplus
}
#endif
#define errorearen_zenbaki (*pk_errno_location())
#define irakurtzeko_soilik_balio 0
#define 쓰기전용 1
#define irakurri_idatzi 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
