#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define skep_lêer open
#define Skep_lêer creat
#define 파일자료읽기 read
#define skryf_lêer_data write
#define sluit_lêer close
#define soek_lêer lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define verwyder_lêer_inskrywing_naam unlink
#define stel_lêer_lengte ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define leesalleen_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define lees_skryf O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define lêer_stand stat
typedef size_t greep_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t lêer_OFFSET_TYPE;
#endif
