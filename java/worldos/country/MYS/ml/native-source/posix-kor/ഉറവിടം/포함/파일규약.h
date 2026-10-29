#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define തുറക്കുക_ഫയല് open
#define സൃഷ്_ടിക്കുക_ഫയല് creat
#define 파일자료읽기 read
#define റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ write
#define അടയ്ക്കുക_ഫയല് close
#define തിരയുക_ഫയല് lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define നീക്കംചെയ്യുക_ഫയല്_എന്_ട്രി_നാ_മം unlink
#define ഗണം_ഫയല്_ദൈര്_ഘ്യം ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define വായന_മാത്രം_മൂല്യം O_RDONLY
#define എഴുതാന്_മാത്രം_മൂല്യം O_WRONLY
#define വായനാ_റൈറ്റ് O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ഫയല്_അവസ്ഥ stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ഫയല്_ഓഫ്_സെറ്റ്_ടൈപ്പ്_ചെയ്യുക;
#endif
