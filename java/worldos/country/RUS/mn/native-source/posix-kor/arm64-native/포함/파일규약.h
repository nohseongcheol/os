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
typedef int64_t файл_Оффсет_бичих;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_Оффсет_бичих pk_lseek(int fd, файл_Оффсет_бичих offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_Оффсет_бичих size);
int pk_fsync(int fd);
int pk_size(int fd);
int нээх_файл(const char *ЗАМ, int арга_горим, ...);
입출력결과형 파일자료읽기(int Файл, void *өгөгдөл, size_t 개수);
입출력결과형 бичих_файл_өгөгдөл(int Файл, const void *өгөгдөл, size_t 개수);
int хаах_файл(int Файл);
файл_Оффсет_бичих хайх_файл(int Файл, файл_Оффсет_бичих 거리, int 기준);
int арилгах_файл_оролт_нэр(const char *ЗАМ);
int багц_файл_урт(int Файл, файл_Оффсет_бичих Хэмжээ);
int 파일저장확정(int Файл);
int файл_хэмжээ(int Файл);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define зөвхөн_унших_утга 0
#define 쓰기전용 1
#define унших_бичих 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
