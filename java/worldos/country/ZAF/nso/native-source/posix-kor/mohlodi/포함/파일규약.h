#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define bula_faele open
#define 파일만들기 creat
#define 파일자료읽기 read
#define ngwala_faele_data write
#define tswalela_faele close
#define nyaka_faele lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define tloša_faele_go_tsenya_tshedimošo_leina unlink
#define sehlopha_faele_botelele ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define balwago_fela_boleng O_RDONLY
#define 쓰기전용 O_WRONLY
#define bala_ngwala O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define faele_boemo stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t faele_E_Šetšego_thaepa;
#endif
