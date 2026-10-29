#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t бајт_COUNT_TYPE;
typedef int64_t датотека_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
датотека_OFFSET_TYPE pk_lseek(int fd, датотека_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, датотека_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int отвори_датотека(const char *ПАТЕКА, int метод_MODE, ...);
입출력결과형 파일자료읽기(int Датотека, void *податоци, size_t ставка_COUNT);
입출력결과형 запиши_датотека_податоци(int Датотека, const void *податоци, size_t ставка_COUNT);
int затвори_датотека(int Датотека);
датотека_OFFSET_TYPE пребарај_датотека(int Датотека, датотека_OFFSET_TYPE 거리, int Project_корен);
int отстрани_датотека_внес_име(const char *ПАТЕКА);
int збир_датотека_должина(int Датотека, датотека_OFFSET_TYPE Големина);
int 파일저장확정(int Датотека);
int датотека_големина(int Датотека);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define само_за_читање_VALUE 0
#define 쓰기전용 1
#define чита_пишува 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
