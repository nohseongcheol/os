#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t байт_СЧЁТ_ТИП;
typedef int64_t файл_СМЕЩ_ТИП;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
файл_СМЕЩ_ТИП pk_lseek(int fd, файл_СМЕЩ_ТИП offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, файл_СМЕЩ_ТИП size);
int pk_fsync(int fd);
int pk_size(int fd);
int открыть_файл(const char *путь, int метод_МОДА, ...);
입출력결과형 чтение_файл_данные(int файл, void *данные, size_t товар_СЧЁТ);
입출력결과형 запись_файл_данные(int файл, const void *данные, size_t товар_СЧЁТ);
int Close_файл(int файл);
файл_СМЕЩ_ТИП поиск_файл(int файл, файл_СМЕЩ_ТИП 거리, int задача_корень);
int удалить_файл_ввод_имя(const char *путь);
int сет_файл_длина(int файл, файл_СМЕЩ_ТИП Размер);
int фиксация_Файлы(int файл);
int размер_файла(int файл);
#ifdef __cplusplus
}
#endif
#define номер_ошибки (*pk_errno_location())
#define нередактируемый_ЗНАЧЕН 0
#define доступный_только_на_запись_ЗНАЧЕН 1
#define для_чтения_и_записи 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define усечь_Оглавление 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define текущий_корень 1
#define элемент_origin 2
#endif
