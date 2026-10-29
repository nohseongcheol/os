#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t beit_COUNT_TYPE;
typedef int64_t ffeil_OFFSET_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ffeil_OFFSET_TYPE pk_lseek(int fd, ffeil_OFFSET_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ffeil_OFFSET_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int agor_ffeil(const char *LLWYBR, int dull_MODE, ...);
입출력결과형 파일자료읽기(int Ffeil, void *data, size_t eitem_COUNT);
입출력결과형 ysgrifennu_ffeil_data(int Ffeil, const void *data, size_t eitem_COUNT);
int cau_ffeil(int Ffeil);
ffeil_OFFSET_TYPE chwilio_ffeil(int Ffeil, ffeil_OFFSET_TYPE 거리, int prosiect_gwraidd);
int tynnu_ffeil_cofnod_enw(const char *LLWYBR);
int set_ffeil_hyd(int Ffeil, ffeil_OFFSET_TYPE Maint);
int 파일저장확정(int Ffeil);
int ffeil_newid_maint(int Ffeil);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define darllen_yn_unig_VALUE 0
#define 쓰기전용 1
#define darllen_ysgrifennu 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
