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
typedef int64_t קובץ_היסט_כתב;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
קובץ_היסט_כתב pk_lseek(int fd, קובץ_היסט_כתב offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, קובץ_היסט_כתב size);
int pk_fsync(int fd);
int pk_size(int fd);
int פתח_קובץ(const char *נתיב, int פעולת_שירות_מצב, ...);
입출력결과형 파일자료읽기(int קובץ, void *נתונים, size_t 개수);
입출력결과형 כתיבה_קובץ_נתונים(int קובץ, const void *נתונים, size_t 개수);
int סגור_קובץ(int קובץ);
קובץ_היסט_כתב חפש_קובץ(int קובץ, קובץ_היסט_כתב 거리, int לשקף_בסיס);
int הסר_קובץ_ערך_שם(const char *נתיב);
int 파일길이정하기(int קובץ, קובץ_היסט_כתב גודל);
int 파일저장확정(int קובץ);
int גודל_קובץ(int קובץ);
#ifdef __cplusplus
}
#endif
#define מספר_שגיאה (*pk_errno_location())
#define לקריאה_בלבד_ערך 0
#define כתיבה_בלבד_ערך 1
#define קריאה_כתיבה 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define נוכחי_בסיס 1
#define סיים_שיחה_מקור 2
#endif
