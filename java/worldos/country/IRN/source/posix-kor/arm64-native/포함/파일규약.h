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
typedef int64_t فایل_جابجایی_لایه_ای_تایپ_کردن;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
فایل_جابجایی_لایه_ای_تایپ_کردن pk_lseek(int fd, فایل_جابجایی_لایه_ای_تایپ_کردن offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, فایل_جابجایی_لایه_ای_تایپ_کردن size);
int pk_fsync(int fd);
int pk_size(int fd);
int ایجاد_فایل(const char *مسیر, int روش_حالت, ...);
입출력결과형 파일자료읽기(int پرونده, void *داده_ها, size_t 개수);
입출력결과형 نوشتن_فایل_داده_ها(int پرونده, const void *داده_ها, size_t 개수);
int بستن_فایل(int پرونده);
فایل_جابجایی_لایه_ای_تایپ_کردن جستجو_کردن_فایل(int پرونده, فایل_جابجایی_لایه_ای_تایپ_کردن 거리, int نمایش_دادن_جذر);
int حذف_فایل_ورودی_نام(const char *مسیر);
int مجموعه_فایل_طول(int پرونده, فایل_جابجایی_لایه_ای_تایپ_کردن اندازه);
int 파일저장확정(int پرونده);
int فایل_اندازه_کردن(int پرونده);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define فقط_خواندنی_مقدار 0
#define 쓰기전용 1
#define خواندن_نوشتن 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
