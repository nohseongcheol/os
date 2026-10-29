#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define فتح_ملف open
#define فتح_ملف_e47823fb creat
#define يقرأ_ملف_بيانات read
#define كتابة_ملف_بيانات write
#define يغلق_ملف close
#define يبحث_ملف lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define يزيل_ملف_إدخال_اسم unlink
#define 파일길이정하기 ftruncate
#define تثبيت_تخزين_الملفات fsync
#define يقرأ_ملف_توفر fstat
#define 파일서술자제어 fcntl
#define للقراءة_فقط_قيمة O_RDONLY
#define 쓰기전용 O_WRONLY
#define مقروء_مكتوب O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define يقتطع_المحتويات O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define حديث_جذر SEEK_CUR
#define إنهاء_مكالمة_نقطة_الأصل SEEK_END
#define حالة_الملف stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ملف_إزاحة_نوع;
#endif
