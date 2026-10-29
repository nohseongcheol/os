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
typedef int64_t ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക pk_lseek(int fd, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക size);
int pk_fsync(int fd);
int pk_size(int fd);
int തുറക്കുക_ഫയല്(const char *വഴി, int విధానం_മോഡ്, ...);
입출력결과형 파일자료읽기(int ഫയല്, void *ഡാറ്റാ, size_t 개수);
입출력결과형 റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(int ഫയല്, const void *ഡാറ്റാ, size_t 개수);
int അടയ്ക്കുക_ഫയല്(int ഫയല്);
ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക തിരയുക_ഫയല്(int ഫയല്, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക 거리, int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം);
int നീക്കംചെയ്യുക_ഫയല്_എന്_ട്രി_നാ_മം(const char *വഴി);
int ഗണം_ഫയല്_ദൈര്_ഘ്യം(int ഫയല്, ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക വലിപ്പം);
int 파일저장확정(int ഫയല്);
int ഫയല്_വലുപ്പം_ക്രമീകരിക്കുക(int ഫയല്);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define വായന_മാത്രം_മൂല്യം 0
#define എഴുതാന്_മാത്രം_മൂല്യം 1
#define വായനാ_റൈറ്റ് 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
