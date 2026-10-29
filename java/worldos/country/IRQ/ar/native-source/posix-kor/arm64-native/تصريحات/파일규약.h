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
typedef int64_t ملف_إزاحة_نوع;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ملف_إزاحة_نوع pk_lseek(int fd, ملف_إزاحة_نوع offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ملف_إزاحة_نوع size);
int pk_fsync(int fd);
int pk_size(int fd);
int فتح_ملف(const char *مسار, int أسلوب_الوضع, ...);
입출력결과형 يقرأ_ملف_بيانات(int ملف, void *بيانات, size_t 개수);
입출력결과형 كتابة_ملف_بيانات(int ملف, const void *بيانات, size_t 개수);
int يغلق_ملف(int ملف);
ملف_إزاحة_نوع يبحث_ملف(int ملف, ملف_إزاحة_نوع 거리, int يعرض_جذر);
int يزيل_ملف_إدخال_اسم(const char *مسار);
int 파일길이정하기(int ملف, ملف_إزاحة_نوع حجم);
int تثبيت_تخزين_الملفات(int ملف);
int حجم_الملف(int ملف);
#ifdef __cplusplus
}
#endif
#define رقم_الخطأ (*pk_errno_location())
#define للقراءة_فقط_قيمة 0
#define 쓰기전용 1
#define مقروء_مكتوب 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define يقتطع_المحتويات 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define حديث_جذر 1
#define إنهاء_مكالمة_نقطة_الأصل 2
#endif
