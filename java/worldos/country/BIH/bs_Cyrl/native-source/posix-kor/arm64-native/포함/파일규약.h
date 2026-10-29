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
int отворити_фајл(const char *пут, int 방식, ...);
입출력결과형 파일자료읽기(int фајл, void *подаци, size_t 개수);
입출력결과형 писати_фајл_подаци(int фајл, const void *подаци, size_t 개수);
int затворити_фајл(int фајл);
파일위치형 претражити_фајл(int фајл, 파일위치형 거리, int 기준);
int уклонити_фајл_унос_назив(const char *пут);
int именовани_скуп_фајл_дужина(int фајл, 파일위치형 подесити_величину);
int 파일저장확정(int фајл);
int фајл_подесити_величину(int фајл);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define само_за_читање_вриједност 0
#define 쓰기전용 1
#define и_за_читање_и_за_писање 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
