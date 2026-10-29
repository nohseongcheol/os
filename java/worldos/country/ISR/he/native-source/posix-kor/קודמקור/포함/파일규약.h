#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define פתח_קובץ open
#define ליצור_קובץ creat
#define 파일자료읽기 read
#define כתיבה_קובץ_נתונים write
#define סגור_קובץ close
#define חפש_קובץ lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define הסר_קובץ_ערך_שם unlink
#define 파일길이정하기 ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define לקריאה_בלבד_ערך O_RDONLY
#define כתיבה_בלבד_ערך O_WRONLY
#define קריאה_כתיבה O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define נוכחי_בסיס SEEK_CUR
#define סיים_שיחה_מקור SEEK_END
#define קובץ_מצב stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t קובץ_היסט_כתב;
#endif
