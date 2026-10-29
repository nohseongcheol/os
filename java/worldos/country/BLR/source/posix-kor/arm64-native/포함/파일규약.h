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
typedef int64_t файл_Зрух_друкаваць;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_Зрух_друкаваць pk_lseek(int fd, файл_Зрух_друкаваць offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_Зрух_друкаваць size);
int pk_fsync(int fd);
int pk_size(int fd);
int адкрыць_файл(const char *ШЛЯХ, int спосаб_рэжым, ...);
입출력결과형 파일자료읽기(int Файл, void *дадзеныя, size_t 개수);
입출력결과형 напісаць_файл_дадзеныя(int Файл, const void *дадзеныя, size_t 개수);
int закрыць_файл(int Файл);
файл_Зрух_друкаваць шукаць_файл(int Файл, файл_Зрух_друкаваць 거리, int 기준);
int выдаліць_файл_увядзенне_імя(const char *ШЛЯХ);
int набор_файл_даўжыня(int Файл, файл_Зрух_друкаваць Памер);
int 파일저장확정(int Файл);
int файл_памер(int Файл);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define толькі_для_чытання_значэнне 0
#define 쓰기전용 1
#define для_чытання_для_запісу 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
