#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t बायट_COUNT_TYPE;
typedef int64_t फायल_ऑफसॅट_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
फायल_ऑफसॅट_TYPE pk_lseek(int fd, फायल_ऑफसॅट_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, फायल_ऑफसॅट_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int उगडचें_फायल(const char *पाथ, int पद्दत_मोड, ...);
입출력결과형 파일자료읽기(int फायल, void *डेटा, size_t आयटम_COUNT);
입출력결과형 बरोवचें_फायल_डेटा(int फायल, const void *डेटा, size_t आयटम_COUNT);
int शेवट_फायल(int फायल);
फायल_ऑफसॅट_TYPE सोद_फायल(int फायल, फायल_ऑफसॅट_TYPE 거리, int प्रॉजॅक्ट_रूट);
int काडचें_फायल_प्रवेश_नांव(const char *पाथ);
int संच_फायल_लांबाय(int फायल, फायल_ऑफसॅट_TYPE आवाठ);
int 파일저장확정(int फायल);
int फायल_आवाठ(int फायल);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define फकत_वाचचें_मोल 0
#define 쓰기전용 1
#define वाचन_बरप 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
