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
typedef int64_t ფაილი_ოფსეტი_აკრეფა;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ფაილი_ოფსეტი_აკრეფა pk_lseek(int fd, ფაილი_ოფსეტი_აკრეფა offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ფაილი_ოფსეტი_აკრეფა size);
int pk_fsync(int fd);
int pk_size(int fd);
int გახსნა_ფაილი(const char *გეზი, int მეთოდი_რეჟიმი, ...);
입출력결과형 파일자료읽기(int ფაილი, void *მონაცემები, size_t 개수);
입출력결과형 ჩაწერა_ფაილი_მონაცემები(int ფაილი, const void *მონაცემები, size_t 개수);
int დახურვა_ფაილი(int ფაილი);
ფაილი_ოფსეტი_აკრეფა ძებნა_ფაილი(int ფაილი, ფაილი_ოფსეტი_აკრეფა 거리, int პროეცირება_ფესვი);
int ამოშლა_ფაილი_შენატანი_სახელი(const char *გეზი);
int ნაკრები_ფაილი_სიგრძე(int ფაილი, ფაილი_ოფსეტი_აკრეფა ზომა);
int 파일저장확정(int ფაილი);
int ფაილი_ზომის_შეცვლა(int ფაილი);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define მხოლოდ_კითხვადი_მნიშვნელობა 0
#define 쓰기전용 1
#define ჩაწერა_წაკითხვა 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
