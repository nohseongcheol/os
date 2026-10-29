#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ашу_файл open
#define жасау_файл creat
#define 파일자료읽기 read
#define жазу_файл_деректер write
#define Жабу_файл close
#define іздеу_файл lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define жою_файл_енгізу_аты unlink
#define жинақ_файл_ұзындық ftruncate
#define бекіту_файл_сақтау_орны fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define тек_оқу_үшін_мән O_RDONLY
#define 쓰기전용 O_WRONLY
#define оқу_жазу O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define қысқарту_Мазмұны O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define ток_түбір SEEK_CUR
#define 끝기준 SEEK_END
#define файл_күй stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t файл_жылжыту_Түрі;
#endif
