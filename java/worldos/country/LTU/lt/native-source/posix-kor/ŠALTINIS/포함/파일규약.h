#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define kurti_Failas open
#define kurti_Failas_e47823fb creat
#define 파일자료읽기 read
#define rašymas_Failas_duomenys write
#define Uždaryti_Failas close
#define ieškoti_Failas lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define pašalinti_Failas_įrašas_pavadinimas unlink
#define 파일길이정하기 ftruncate
#define vykdymas_failų_saugykla fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define tik_skaitomas_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define trumpinti_Turinys O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define dabartinis_šaknis SEEK_CUR
#define 끝기준 SEEK_END
#define Failas_būsena stat
typedef size_t baitas_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Failas_OFFSET_TYPE;
#endif
