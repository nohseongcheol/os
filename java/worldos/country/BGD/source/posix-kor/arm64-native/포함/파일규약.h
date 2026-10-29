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
typedef int64_t ফাইল_অফসেট_টাইপ_করুন;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ফাইল_অফসেট_টাইপ_করুন pk_lseek(int fd, ফাইল_অফসেট_টাইপ_করুন offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ফাইল_অফসেট_টাইপ_করুন size);
int pk_fsync(int fd);
int pk_size(int fd);
int খোলা_ফাইল(const char *পথ_2, int পদ্ধতি_মোড, ...);
입출력결과형 파일자료읽기(int নথির_নাম, void *ডাটা, size_t 개수);
입출력결과형 লেখা_ফাইল_ডাটা(int নথির_নাম, const void *ডাটা, size_t 개수);
int বন্ধ_ফাইল(int নথির_নাম);
ফাইল_অফসেট_টাইপ_করুন সিক_ফাইল(int নথির_নাম, ফাইল_অফসেট_টাইপ_করুন 거리, int প্রকল্প_মূল);
int সরানো_ফাইল_ভুক্তি_নাম(const char *পথ_2);
int সেট_ফাইল_দৈর্ঘ্য(int নথির_নাম, ফাইল_অফসেট_টাইপ_করুন আকার);
int 파일저장확정(int নথির_নাম);
int ফাইল_আয়তন(int নথির_নাম);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define কেবল_পাঠযোগ্য_মান 0
#define 쓰기전용 1
#define পঠন_লিখন 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
