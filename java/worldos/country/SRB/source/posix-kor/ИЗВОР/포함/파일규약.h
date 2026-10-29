#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define креирати_фајл open
#define Направи_фајл creat
#define 파일자료읽기 read
#define писати_фајл_подаци write
#define затварање_фајл close
#define тражити_фајл lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define уклонити_фајл_унос_име unlink
#define скуп_фајл_дужина ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define само_за_читање_вриједност O_RDONLY
#define 쓰기전용 O_WRONLY
#define за_читање_писање O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define актуелно_корен SEEK_CUR
#define 끝기준 SEEK_END
#define фајл_стање stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t фајл_Помак_тип;
#endif
