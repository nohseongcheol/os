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
typedef int64_t ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න pk_lseek(int fd, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න size);
int pk_fsync(int fd);
int pk_size(int fd);
int සාදන්න_ගොනුව(const char *මාර්_ගය, int ක්_රමය_ප්_රකාරය, ...);
입출력결과형 파일자료읽기(int ගොනු, void *දත්ත, size_t 개수);
입출력결과형 ලියන්න_ගොනුව_දත්ත(int ගොනු, const void *දත්ත, size_t 개수);
int වසන්න_ගොනුව(int ගොනු);
ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න සොයන්න_ගොනුව(int ගොනු, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න 거리, int 기준);
int ඉවත්_කරන්න_ගොනුව_පිවිසුම_නම(const char *මාර්_ගය);
int කට්ටලය_ගොනුව_දිග(int ගොනු, ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න ප්_රමාණය);
int 파일저장확정(int ගොනු);
int ගොනුව_ප්_රමාණනය(int ගොනු);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define කියවීම්_පමණි_අගය 0
#define 쓰기전용 1
#define කියවීම්_ලිවීම් 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
