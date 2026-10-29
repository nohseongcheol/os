#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <основные_определения.h>
#include <система/типы_данных.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void немедленно_завершить(int состояние) __attribute__((noreturn));
ssize_t читать(int дескриптор_файла, void *буфер_передачи, size_t count);
ssize_t писать(int дескриптор_файла, const void *буфер_передачи, size_t count);
int закрыть(int дескриптор_файла);
off_t переместить_позицию_файла(int дескриптор_файла, off_t offset, int whence);
pid_t создать_дочерний_процесс(void);
int заменить_исполняемую_программу(const char *путь, char *const аргументы_2[], char *const envp[]);
pid_t получить_номер_процесса(void);
pid_t получить_номер_родительского_процесса(void);
uid_t получить_номер_пользователя(void);
uid_t получить_действующий_номер_пользователя(void);
gid_t получить_номер_группы(void);
gid_t получить_действующий_номер_группы(void);
int проверить_права_доступа(const char *путь, int mode);
int сменить_рабочий_каталог(const char *путь);
char *получить_путь_рабочего_каталога(char *буфер_передачи, size_t число_цифр);
int дублировать_ссылку_на_открытый_файл(int дескриптор_файла);
int дублировать_ссылку_под_заданным_номером(int oldfd, int newfd);
int согласовать_данные_файла(int дескриптор_файла);
void согласовать_все_данные(void);
int проверить_является_ли_терминалом(int дескриптор_файла);
int задать_конец_динамической_памяти(void *address);
void *сместить_конец_динамической_памяти(int increment);
#ifdef __cplusplus
}
#endif

#endif
