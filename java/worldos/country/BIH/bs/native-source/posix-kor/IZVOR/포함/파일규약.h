#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define kreirati_fajl open
#define Create_fajl creat
#define 파일자료읽기 read
#define pisati_fajl_podaci write
#define zatvoriti_fajl close
#define tražiti_fajl lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ukloniti_fajl_unos_naziv unlink
#define skup_fajl_dužina ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define samo_za_čitanje_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define i_za_čitanje_i_za_pisanje O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define trenutno_koijen SEEK_CUR
#define 끝기준 SEEK_END
#define fajl_stanje stat
typedef size_t bajt_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t fajl_Pomak_TYPE;
#endif
