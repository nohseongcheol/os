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
typedef int64_t ફાઇલ_ઑફસેટ_લખો;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ફાઇલ_ઑફસેટ_લખો pk_lseek(int fd, ફાઇલ_ઑફસેટ_લખો offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ફાઇલ_ઑફસેટ_લખો size);
int pk_fsync(int fd);
int pk_size(int fd);
int બનાવો_ફાઇલ(const char *પથ, int પદ્ધતિ_મોડ, ...);
입출력결과형 파일자료읽기(int ફાઈલ, void *ડેટા, size_t 개수);
입출력결과형 લખો_ફાઇલ_ડેટા(int ફાઈલ, const void *ડેટા, size_t 개수);
int બંધ_કરો_ફાઇલ(int ફાઈલ);
ફાઇલ_ઑફસેટ_લખો સીક_ફાઇલ(int ફાઈલ, ફાઇલ_ઑફસેટ_લખો 거리, int પ્રોજેક્ટ_રૂટ);
int કાઢી_નાંખો_ફાઇલ_પ્રવેશ_નામ(const char *પથ);
int સેટ_ફાઇલ_લંબાઈ(int ફાઈલ, ફાઇલ_ઑફસેટ_લખો માપ);
int 파일저장확정(int ફાઈલ);
int ફાઇલ_આકાર(int ફાઈલ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ફક્ત_વાંચવા_માટે_મૂલ્ય 0
#define 쓰기전용 1
#define વાંચન_લેખન 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
