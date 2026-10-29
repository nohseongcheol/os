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
typedef int64_t файл_жылжыту_Түрі;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_жылжыту_Түрі pk_lseek(int fd, файл_жылжыту_Түрі offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_жылжыту_Түрі size);
int pk_fsync(int fd);
int pk_size(int fd);
int ашу_файл(const char *Жол_2, int әдіс_режим, ...);
입출력결과형 파일자료읽기(int Файл, void *деректер, size_t 개수);
입출력결과형 жазу_файл_деректер(int Файл, const void *деректер, size_t 개수);
int Жабу_файл(int Файл);
файл_жылжыту_Түрі іздеу_файл(int Файл, файл_жылжыту_Түрі 거리, int жоба_түбір);
int жою_файл_енгізу_аты(const char *Жол_2);
int жинақ_файл_ұзындық(int Файл, файл_жылжыту_Түрі Өлшемі);
int бекіту_файл_сақтау_орны(int Файл);
int файл_өлшемі(int Файл);
#ifdef __cplusplus
}
#endif
#define қате_нөмірі (*pk_errno_location())
#define тек_оқу_үшін_мән 0
#define 쓰기전용 1
#define оқу_жазу 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define қысқарту_Мазмұны 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define ток_түбір 1
#define 끝기준 2
#endif
