#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define sos_bara_denc open
#define sos_bara_denc_e47823fb creat
#define 파일자료읽기 read
#define biir_bara_denc_mbir write
#define Tej_bara_denc close
#define seet_bara_denc lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define dandal_bara_denc_dugal_xabaar_tur unlink
#define Boole_gi_bara_denc_diir ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ngir_jaŋarek_la_xëyma O_RDONLY
#define 쓰기전용 O_WRONLY
#define jàng_bind O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define bara_denc_nekkin stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t bara_denc_Randal_xeet;
#endif
