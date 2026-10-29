#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define отварям_Файл open
#define Създаване_Файл creat
#define 파일자료읽기 read
#define записване_Файл_данни write
#define затварям_Файл close
#define търся_Файл lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define премахвам_Файл_запис_препратка_към_клетка unlink
#define 파일길이정하기 ftruncate
#define фиксиране_място_за_съхранение_на_файлове fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define само_за_четене_стойност O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define съкращавам_Съдържание O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define в_срок_корен SEEK_CUR
#define 끝기준 SEEK_END
#define Файл_статус stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t Файл_Изместване_Тип;
#endif
