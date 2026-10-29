#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define otvoreno_Datoteka open
#define Create_Datoteka creat
#define 파일자료읽기 read
#define zapisivanje_Datoteka_podaci write
#define Zatvori_Datoteka close
#define tražiti_Datoteka lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ukloniti_Datoteka_unos_naziv unlink
#define 파일길이정하기 ftruncate
#define izvršavanje_pohrana_datoteka fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define samo_za_čitanje_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define skratiti_Sadržaj O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define redovno_korijen SEEK_CUR
#define 끝기준 SEEK_END
#define Datoteka_stanje stat
typedef size_t bajt_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Datoteka_pomak_TYPE;
#endif
