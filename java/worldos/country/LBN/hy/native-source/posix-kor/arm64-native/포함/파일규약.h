#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t 바이트수형;
typedef int64_t նիշք_Տեղաշարժում_մուտքագրել;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
նիշք_Տեղաշարժում_մուտքագրել pk_lseek(int fd, նիշք_Տեղաշարժում_մուտքագրել offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, նիշք_Տեղաշարժում_մուտքագրել size);
int pk_fsync(int fd);
int pk_size(int fd);
int բացել_նիշք(const char *Ճանապարհ, int եղանակ_կերպ, ...);
입출력결과형 파일자료읽기(int Ֆայլ, void *տվյալ, size_t 개수);
입출력결과형 գրել_նիշք_տվյալ(int Ֆայլ, const void *տվյալ, size_t 개수);
int փակել_նիշք(int Ֆայլ);
նիշք_Տեղաշարժում_մուտքագրել որոնել_նիշք(int Ֆայլ, նիշք_Տեղաշարժում_մուտքագրել 거리, int արձակել_արմատ);
int հեռացնել_նիշք_մուտքագրում_անուն(const char *Ճանապարհ);
int կազմ_նիշք_տեւողություն(int Ֆայլ, նիշք_Տեղաշարժում_մուտքագրել Չափս);
int 파일저장확정(int Ֆայլ);
int նիշք_չափափոխել(int Ֆայլ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define միայն_կարդալու_արժեք 0
#define 쓰기전용 1
#define կարդալ_գրել 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
