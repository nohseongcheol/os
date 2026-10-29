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
typedef int64_t ফাইল_অফছেট_প্ৰকাৰ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ফাইল_অফছেট_প্ৰকাৰ pk_lseek(int fd, ফাইল_অফছেট_প্ৰকাৰ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ফাইল_অফছেট_প্ৰকাৰ size);
int pk_fsync(int fd);
int pk_size(int fd);
int খোলক_ফাইল(const char *পথ, int পদ্ধতি_মোড, ...);
입출력결과형 파일자료읽기(int নথিপত্ৰ, void *ডাটা, size_t 개수);
입출력결과형 লিখক_ফাইল_ডাটা(int নথিপত্ৰ, const void *ডাটা, size_t 개수);
int বন্ধ_কৰক_ফাইল(int নথিপত্ৰ);
ফাইল_অফছেট_প্ৰকাৰ ছীক_ফাইল(int নথিপত্ৰ, ফাইল_অফছেট_প্ৰকাৰ 거리, int 기준);
int আঁতৰাওক_ফাইল_প্রবিষ্ট_নাম(const char *পথ);
int ছেট_ফাইল_দৈর্ঘ্য(int নথিপত্ৰ, ফাইল_অফছেট_প্ৰকাৰ মাপ);
int 파일저장확정(int নথিপত্ৰ);
int ফাইল_আকাৰ_কৰক(int নথিপত্ৰ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ৰিড_অনলি_মান 0
#define 쓰기전용 1
#define পঢ়িব_লিখিব_পৰা 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
