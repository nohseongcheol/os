#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define unda_faili open
#define unda_faili_e47823fb creat
#define 파일자료읽기 read
#define andika_faili_data write
#define funga_faili close
#define tafuta_faili lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ondoa_faili_ingizo_jina unlink
#define seti_faili_urefu ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define soma_tu_thamani O_RDONLY
#define 쓰기전용 O_WRONLY
#define soma_andika O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define faili_hali stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t faili_Chipua_aina;
#endif
