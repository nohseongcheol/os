#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bajt_COUNT_Tip;
typedef int64_t Datoteka_odmik_Tip;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Datoteka_odmik_Tip pk_lseek(int fd, Datoteka_odmik_Tip offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Datoteka_odmik_Tip size);
int pk_fsync(int fd);
int pk_size(int fd);
int odprto_Datoteka(const char *POT, int metoda_MODE, ...);
입출력결과형 파일자료읽기(int Datoteka, void *podatki, size_t element_COUNT);
입출력결과형 pisati_Datoteka_podatki(int Datoteka, const void *podatki, size_t element_COUNT);
int Zapri_Datoteka(int Datoteka);
Datoteka_odmik_Tip iskati_Datoteka(int Datoteka, Datoteka_odmik_Tip 거리, int pobuda_koren);
int odstraniti_Datoteka_vnos_ime(const char *POT);
int 파일길이정하기(int Datoteka, Datoteka_odmik_Tip Velikost);
int potrjevanje_datotečna_shramba(int Datoteka);
int velikost_datoteke(int Datoteka);
#ifdef __cplusplus
}
#endif
#define številka_napake (*pk_errno_location())
#define samo_za_branje_VALUE 0
#define 쓰기전용 1
#define branje_pisanje 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define sprotno_koren 1
#define 끝기준 2
#endif
