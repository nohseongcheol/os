#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t 바이트수형;
typedef int64_t 파일위치형;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
파일위치형 pk_lseek(int fd, 파일위치형 offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, 파일위치형 size);
int pk_fsync(int fd);
int pk_size(int fd);
int matuirli_ini(const char *aqqut, int 방식, ...);
입출력결과형 파일자료읽기(int ini, void *titiqqat, size_t 개수);
입출력결과형 titiraq_ini_titiqqat(int ini, const void *titiqqat, size_t 개수);
int matuli_ini(int ini);
파일위치형 qinirli_ini(int ini, 파일위치형 거리, int 기준);
int sanirvalli_ini_Iliniku_atiq(const char *aqqut);
int attiqsimaniit_ini_takininga(int ini, 파일위치형 anininga);
int 파일저장확정(int ini);
int ini_anininga(int ini);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define takugatuinnaq_atuutilik 0
#define 쓰기전용 1
#define uqalimaarli_titirarli 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
