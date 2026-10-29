#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_COUNT_TYPE;
typedef int64_t Fails_Nobīde_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fails_Nobīde_TYPE pk_lseek(int fd, Fails_Nobīde_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fails_Nobīde_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int atvērt_Fails(const char *CEĻŠ, int metode_MODE, ...);
입출력결과형 파일자료읽기(int Fails, void *dati, size_t krājums_COUNT);
입출력결과형 rakstīšana_Fails_dati(int Fails, const void *dati, size_t krājums_COUNT);
int Aizvērt_Fails(int Fails);
Fails_Nobīde_TYPE meklēt_Fails(int Fails, Fails_Nobīde_TYPE 거리, int Project_sakne);
int noņemt_Fails_ievade_nosaukums(const char *CEĻŠ);
int 파일길이정하기(int Fails, Fails_Nobīde_TYPE Izmērs);
int izpilde_failu_krātuve(int Fails);
int faila_lielums(int Fails);
#ifdef __cplusplus
}
#endif
#define kļūdas_numurs (*pk_errno_location())
#define tikai_lasāms_VALUE 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define apraut_Satura_rādītājs 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define pašreizējais_sakne 1
#define 끝기준 2
#endif
