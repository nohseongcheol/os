#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define เปิด_แฟ้ม open
#define เปิด_แฟ้ม_e47823fb creat
#define 파일자료읽기 read
#define 파일자료쓰기 write
#define ปิด_แฟ้ม close
#define กรอ_แฟ้ม lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define นําออก_แฟ้ม_รายการ_ชื่อ unlink
#define 파일길이정하기 ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define อ่านอย่างเดียว_ค่า O_RDONLY
#define แบบเขียนอย่างเดียว_ค่า O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define ปัจจุบัน_ราก SEEK_CUR
#define 끝기준 SEEK_END
#define แฟ้ม_สถานะ stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t แฟ้ม_ออฟเซต_ชนิด;
#endif
