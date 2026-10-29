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
typedef int64_t файл_Жылбышуу_түрү;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_Жылбышуу_түрү pk_lseek(int fd, файл_Жылбышуу_түрү offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_Жылбышуу_түрү size);
int pk_fsync(int fd);
int pk_size(int fd);
int ачуу_файл(const char *ЖОЛ, int ыкма_режим, ...);
입출력결과형 파일자료읽기(int Файл, void *берилмелер, size_t 개수);
입출력결과형 жазуу_файл_берилмелер(int Файл, const void *берилмелер, size_t 개수);
int жабуу_файл(int Файл);
файл_Жылбышуу_түрү издөө_файл(int Файл, файл_Жылбышуу_түрү 거리, int 기준);
int алып_салуу_файл_киргизме_жазуу_аты(const char *ЖОЛ);
int топ_файл_узундук(int Файл, файл_Жылбышуу_түрү Өлчөмү);
int 파일저장확정(int Файл);
int файл_көлөм(int Файл);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define окуу_үчүн_гана_маани 0
#define 쓰기전용 1
#define окуу_жазуу 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
