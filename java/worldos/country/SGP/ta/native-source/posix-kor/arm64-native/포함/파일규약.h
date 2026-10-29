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
typedef int64_t கோப்பு_ஆஃப்செட்_வகை;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
கோப்பு_ஆஃப்செட்_வகை pk_lseek(int fd, கோப்பு_ஆஃப்செட்_வகை offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, கோப்பு_ஆஃப்செட்_வகை size);
int pk_fsync(int fd);
int pk_size(int fd);
int திற_கோப்பு(const char *பாதை_2, int முறை_பயன்முறை, ...);
입출력결과형 파일자료읽기(int கோப்பின்_பெயர், void *தரவு, size_t 개수);
입출력결과형 எழுது_கோப்பு_தரவு(int கோப்பின்_பெயர், const void *தரவு, size_t 개수);
int மூடு_கோப்பு(int கோப்பின்_பெயர்);
கோப்பு_ஆஃப்செட்_வகை தேடு_கோப்பு(int கோப்பின்_பெயர், கோப்பு_ஆஃப்செட்_வகை 거리, int திட்டப்பணி_மூலம்);
int அகற்று_கோப்பு_உள்ளீடு_பெயர்(const char *பாதை_2);
int அமை_கோப்பு_நீளம்(int கோப்பின்_பெயர், கோப்பு_ஆஃப்செட்_வகை அளவு);
int 파일저장확정(int கோப்பின்_பெயர்);
int கோப்பு_அளவு(int கோப்பின்_பெயர்);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define படிக்க_மட்டும்_மதிப்பு 0
#define எழுதுதல்_மட்டும்_மதிப்பு 1
#define படிக்க_எழுத 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
