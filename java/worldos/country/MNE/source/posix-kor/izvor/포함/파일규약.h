#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define otvoren_Datoteka open
#define Create_Datoteka creat
#define 파일자료읽기 read
#define 파일자료쓰기 write
#define Zatvori_Datoteka close
#define tražiti_Datoteka lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ukloniti_Datoteka_stavka_ime unlink
#define 파일길이정하기 ftruncate
#define izvršavanje_skladište_datoteka fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define samo_za_čitanje_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define za_čitanje_pisanje O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define aktuelno_koren SEEK_CUR
#define 끝기준 SEEK_END
#define Datoteka_status stat
typedef size_t bajt_COUNT_tip;
typedef ssize_t 입출력결과형;
typedef off_t Datoteka_Pomak_tip;
#endif
