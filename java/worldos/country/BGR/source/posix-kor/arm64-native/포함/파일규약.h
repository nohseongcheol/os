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
typedef int64_t Файл_Изместване_Тип;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Файл_Изместване_Тип pk_lseek(int fd, Файл_Изместване_Тип offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Файл_Изместване_Тип size);
int pk_fsync(int fd);
int pk_size(int fd);
int отварям_Файл(const char *ПЪТ, int метод_режим, ...);
입출력결과형 파일자료읽기(int Файл, void *данни, size_t 개수);
입출력결과형 записване_Файл_данни(int Файл, const void *данни, size_t 개수);
int затварям_Файл(int Файл);
Файл_Изместване_Тип търся_Файл(int Файл, Файл_Изместване_Тип 거리, int проект_корен);
int премахвам_Файл_запис_препратка_към_клетка(const char *ПЪТ);
int 파일길이정하기(int Файл, Файл_Изместване_Тип Размер);
int фиксиране_място_за_съхранение_на_файлове(int Файл);
int размер_на_файл(int Файл);
#ifdef __cplusplus
}
#endif
#define Номер_на_грешка (*pk_errno_location())
#define само_за_четене_стойност 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define съкращавам_Съдържание 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define в_срок_корен 1
#define 끝기준 2
#endif
