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
typedef int64_t فایل_ئۆفسێت_چاپکردن;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
فایل_ئۆفسێت_چاپکردن pk_lseek(int fd, فایل_ئۆفسێت_چاپکردن offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, فایل_ئۆفسێت_چاپکردن size);
int pk_fsync(int fd);
int pk_size(int fd);
int کردنەوە_فایل(const char *گوزەر, int ڕێگا_دۆخ, ...);
입출력결과형 파일자료읽기(int فایل, void *دەیتا, size_t 개수);
입출력결과형 ڕایت_کردن_فایل_دەیتا(int فایل, const void *دەیتا, size_t 개수);
int داخستن_فایل(int فایل);
فایل_ئۆفسێت_چاپکردن گەڕان_فایل(int فایل, فایل_ئۆفسێت_چاپکردن 거리, int 기준);
int لابردن_فایل_تێنووسین_ناو(const char *گوزەر);
int سێت_فایل_درێژی(int فایل, فایل_ئۆفسێت_چاپکردن گۆڕینی_ئەندازە);
int 파일저장확정(int فایل);
int فایل_گۆڕینی_ئەندازە(int فایل);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define تەنیا_دەخوێنرێتەوە_نرخ 0
#define 쓰기전용 1
#define خوێندن_نووسین 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
