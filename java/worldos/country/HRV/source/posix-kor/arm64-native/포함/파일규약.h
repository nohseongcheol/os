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
typedef int64_t Datoteka_pomak_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Datoteka_pomak_TYPE pk_lseek(int fd, Datoteka_pomak_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Datoteka_pomak_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int otvoreno_Datoteka(const char *PUTANJA, int postupak_MODE, ...);
입출력결과형 파일자료읽기(int Datoteka, void *podaci, size_t artikl_COUNT);
입출력결과형 zapisivanje_Datoteka_podaci(int Datoteka, const void *podaci, size_t artikl_COUNT);
int Zatvori_Datoteka(int Datoteka);
Datoteka_pomak_TYPE tražiti_Datoteka(int Datoteka, Datoteka_pomak_TYPE 거리, int akcija_korijen);
int ukloniti_Datoteka_unos_naziv(const char *PUTANJA);
int 파일길이정하기(int Datoteka, Datoteka_pomak_TYPE Veličina);
int izvršavanje_pohrana_datoteka(int Datoteka);
int veličina_datoteke(int Datoteka);
#ifdef __cplusplus
}
#endif
#define broj_pogreške (*pk_errno_location())
#define samo_za_čitanje_VALUE 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define skratiti_Sadržaj 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define redovno_korijen 1
#define 끝기준 2
#endif
