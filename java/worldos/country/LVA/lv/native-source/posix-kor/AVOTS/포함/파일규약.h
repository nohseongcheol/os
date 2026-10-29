#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define atvērt_Fails open
#define atvērt_Fails_e47823fb creat
#define 파일자료읽기 read
#define rakstīšana_Fails_dati write
#define Aizvērt_Fails close
#define meklēt_Fails lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define noņemt_Fails_ievade_nosaukums unlink
#define 파일길이정하기 ftruncate
#define izpilde_failu_krātuve fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define tikai_lasāms_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define apraut_Satura_rādītājs O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define pašreizējais_sakne SEEK_CUR
#define 끝기준 SEEK_END
#define Fails_statuss stat
typedef size_t byte_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Fails_Nobīde_TYPE;
#endif
