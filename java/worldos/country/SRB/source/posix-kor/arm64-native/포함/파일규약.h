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
typedef int64_t фајл_Помак_тип;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
фајл_Помак_тип pk_lseek(int fd, фајл_Помак_тип offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, фајл_Помак_тип size);
int pk_fsync(int fd);
int pk_size(int fd);
int креирати_фајл(const char *ПУТАЊА, int метода_мод, ...);
입출력결과형 파일자료읽기(int Датотека, void *подаци, size_t 개수);
입출력결과형 писати_фајл_подаци(int Датотека, const void *подаци, size_t 개수);
int затварање_фајл(int Датотека);
фајл_Помак_тип тражити_фајл(int Датотека, фајл_Помак_тип 거리, int пројектовати_корен);
int уклонити_фајл_унос_име(const char *ПУТАЊА);
int скуп_фајл_дужина(int Датотека, фајл_Помак_тип Величина);
int 파일저장확정(int Датотека);
int фајл_подесити_величину(int Датотека);
#ifdef __cplusplus
}
#endif
#define број_грешке (*pk_errno_location())
#define само_за_читање_вриједност 0
#define 쓰기전용 1
#define за_читање_писање 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define актуелно_корен 1
#define 끝기준 2
#endif
