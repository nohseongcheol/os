#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t baitas_COUNT_TYPE;
typedef int64_t Failas_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Failas_OFFSET_TYPE pk_lseek(int fd, Failas_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Failas_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int kurti_Failas(const char *KELIAS, int metodas_MODE, ...);
입출력결과형 파일자료읽기(int Failas, void *duomenys, size_t prekė_COUNT);
입출력결과형 rašymas_Failas_duomenys(int Failas, const void *duomenys, size_t prekė_COUNT);
int Uždaryti_Failas(int Failas);
Failas_OFFSET_TYPE ieškoti_Failas(int Failas, Failas_OFFSET_TYPE 거리, int Project_šaknis);
int pašalinti_Failas_įrašas_pavadinimas(const char *KELIAS);
int 파일길이정하기(int Failas, Failas_OFFSET_TYPE Dydis);
int vykdymas_failų_saugykla(int Failas);
int failo_dydis(int Failas);
#ifdef __cplusplus
}
#endif
#define klaidos_numeris (*pk_errno_location())
#define tik_skaitomas_VALUE 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define trumpinti_Turinys 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define dabartinis_šaknis 1
#define 끝기준 2
#endif
