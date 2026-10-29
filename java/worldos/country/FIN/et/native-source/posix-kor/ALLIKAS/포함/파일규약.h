#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define avama_Fail open
#define avama_Fail_e47823fb creat
#define 파일자료읽기 read
#define kirjutamine_Fail_andmed write
#define Sule_Fail close
#define otsima_Fail lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define eemaldama_Fail_kirje_nimetus unlink
#define 파일길이정하기 ftruncate
#define kinnitamine_failisalvestusruum fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define kirjutuskaitstud_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define lühendama_Sisu O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define tähtaja_piires_juur SEEK_CUR
#define 끝기준 SEEK_END
#define Fail_olek stat
typedef size_t bait_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Fail_nihe_TYPE;
#endif
