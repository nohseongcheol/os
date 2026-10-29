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
typedef int64_t Файл_Зміщена_копія_Тип;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Файл_Зміщена_копія_Тип pk_lseek(int fd, Файл_Зміщена_копія_Тип offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Файл_Зміщена_копія_Тип size);
int pk_fsync(int fd);
int pk_size(int fd);
int відкрито_Файл(const char *шлях, int метод_режим, ...);
입출력결과형 파일자료읽기(int файл, void *дані, size_t 개수);
입출력결과형 записування_Файл_дані(int файл, const void *дані, size_t 개수);
int Закрити_Файл(int файл);
Файл_Зміщена_копія_Тип шукати_Файл(int файл, Файл_Зміщена_копія_Тип 거리, int Дії_корінь);
int вилучати_Файл_запис_ім_я(const char *шлях);
int 파일길이정하기(int файл, Файл_Зміщена_копія_Тип Розмір);
int затвердження_файлове_сховище(int файл);
int розмір_файлу(int файл);
#ifdef __cplusplus
}
#endif
#define номер_помилки (*pk_errno_location())
#define лише_для_читання_значення 0
#define 쓰기전용 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define скорочувати_Зміст 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define чинний_корінь 1
#define 끝기준 2
#endif
