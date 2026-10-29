#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define opne_fil open
#define Opprett_fil creat
#define 파일자료읽기 read
#define skrive_fil_data write
#define Lukk_fil close
#define søk_fil lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define fjerne_fil_oppføring_namn unlink
#define sett_fil_lengd ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define skriveverna_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define lese_og_skrivetilgang O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define betalt_rot SEEK_CUR
#define avslutte_nullpunkt SEEK_END
#define fil_merkje stat
typedef size_t byte_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t fil_OFFSET_TYPE;
#endif
