#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define খোলক_ফাইল open
#define ক্ৰিয়েট_ফাইল creat
#define 파일자료읽기 read
#define লিখক_ফাইল_ডাটা write
#define বন্ধ_কৰক_ফাইল close
#define ছীক_ফাইল lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define আঁতৰাওক_ফাইল_প্রবিষ্ট_নাম unlink
#define ছেট_ফাইল_দৈর্ঘ্য ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ৰিড_অনলি_মান O_RDONLY
#define 쓰기전용 O_WRONLY
#define পঢ়িব_লিখিব_পৰা O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ফাইল_অৱস্থা stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ফাইল_অফছেট_প্ৰকাৰ;
#endif
