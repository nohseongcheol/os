#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bajt_COUNT_TYPE;
typedef int64_t fajl_Pomak_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fajl_Pomak_TYPE pk_lseek(int fd, fajl_Pomak_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fajl_Pomak_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int kreirati_fajl(const char *Putanja, int metoda_mod, ...);
입출력결과형 파일자료읽기(int Fajl, void *podaci, size_t stavka_COUNT);
입출력결과형 pisati_fajl_podaci(int Fajl, const void *podaci, size_t stavka_COUNT);
int zatvoriti_fajl(int Fajl);
fajl_Pomak_TYPE tražiti_fajl(int Fajl, fajl_Pomak_TYPE 거리, int projicirati_koijen);
int ukloniti_fajl_unos_naziv(const char *Putanja);
int skup_fajl_dužina(int Fajl, fajl_Pomak_TYPE Veličina);
int 파일저장확정(int Fajl);
int fajl_podesiti_veličinu(int Fajl);
#ifdef __cplusplus
}
#endif
#define broj_greške (*pk_errno_location())
#define samo_za_čitanje_VALUE 0
#define 쓰기전용 1
#define i_za_čitanje_i_za_pisanje 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define trenutno_koijen 1
#define 끝기준 2
#endif
