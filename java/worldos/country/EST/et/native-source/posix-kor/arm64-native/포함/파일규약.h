#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bait_COUNT_TYPE;
typedef int64_t Fail_nihe_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fail_nihe_TYPE pk_lseek(int fd, Fail_nihe_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fail_nihe_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int avama_Fail(const char *RADA, int meetod_MODE, ...);
입출력결과형 파일자료읽기(int Fail, void *andmed, size_t kaup_COUNT);
입출력결과형 kirjutamine_Fail_andmed(int Fail, const void *andmed, size_t kaup_COUNT);
int Sule_Fail(int Fail);
Fail_nihe_TYPE otsima_Fail(int Fail, Fail_nihe_TYPE 거리, int Project_juur);
int eemaldama_Fail_kirje_nimetus(const char *RADA);
int 파일길이정하기(int Fail, Fail_nihe_TYPE Suurus);
int kinnitamine_failisalvestusruum(int Fail);
int faili_maht(int Fail);
#ifdef __cplusplus
}
#endif
#define tõrke_number (*pk_errno_location())
#define kirjutuskaitstud_VALUE 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define lühendama_Sisu 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define tähtaja_piires_juur 1
#define 끝기준 2
#endif
