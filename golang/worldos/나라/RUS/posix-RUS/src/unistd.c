#include <errno.h>
#include <fcntl.h>
#include <система/stat.h>
#include <система/ожидание_потомков.h>
#include <unistd.h>
#include <система/syscall.h>

enum {
    SYS_немедленно_завершить = 1,
    SYS_создать_дочерний_процесс = 2,
    SYS_читать = 3,
    SYS_писать = 4,
    SYS_закрыть = 6,
    SYS_заменить_исполняемую_программу = 11,
    SYS_сменить_рабочий_каталог = 12,
    SYS_переместить_позицию_файла = 19,
    SYS_получить_номер_процесса = 20,
    SYS_получить_номер_пользователя = 24,
    SYS_проверить_права_доступа = 33,
    SYS_согласовать_все_данные = 36,
    SYS_дублировать_ссылку_на_открытый_файл = 41,
    SYS_задать_конец_динамической_памяти = 45,
    SYS_получить_номер_группы = 47,
    SYS_получить_действующий_номер_пользователя = 49,
    SYS_получить_действующий_номер_группы = 50,
    SYS_дублировать_ссылку_под_заданным_номером = 63,
    SYS_получить_номер_родительского_процесса = 64,
    SYS_согласовать_данные_файла = 118,
    SYS_получить_путь_рабочего_каталога = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void немедленно_завершить(int состояние)
{
    SC1(SYS_немедленно_завершить, состояние);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t читать(int дескриптор_файла, void *буфер_передачи, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_читать, дескриптор_файла, буфер_передачи, count));
}

ssize_t писать(int дескриптор_файла, const void *буфер_передачи, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_писать, дескриптор_файла, буфер_передачи, count));
}

int закрыть(int дескриптор_файла)
{
    return (int)__syscall_result(SC1(SYS_закрыть, дескриптор_файла));
}

off_t переместить_позицию_файла(int дескриптор_файла, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_переместить_позицию_файла, дескриптор_файла, offset, whence));
}

pid_t создать_дочерний_процесс(void)
{
    return (pid_t)__syscall_result(SC0(SYS_создать_дочерний_процесс));
}

int заменить_исполняемую_программу(const char *путь, char *const аргументы_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_заменить_исполняемую_программу, путь, аргументы_2, envp));
}

pid_t получить_номер_процесса(void) { return (pid_t)SC0(SYS_получить_номер_процесса); }
pid_t получить_номер_родительского_процесса(void) { return (pid_t)SC0(SYS_получить_номер_родительского_процесса); }
uid_t получить_номер_пользователя(void) { return (uid_t)SC0(SYS_получить_номер_пользователя); }
uid_t получить_действующий_номер_пользователя(void) { return (uid_t)SC0(SYS_получить_действующий_номер_пользователя); }
gid_t получить_номер_группы(void) { return (gid_t)SC0(SYS_получить_номер_группы); }
gid_t получить_действующий_номер_группы(void) { return (gid_t)SC0(SYS_получить_действующий_номер_группы); }

int проверить_права_доступа(const char *путь, int mode)
{
    return (int)__syscall_result(SC2(SYS_проверить_права_доступа, путь, mode));
}

int сменить_рабочий_каталог(const char *путь)
{
    return (int)__syscall_result(SC1(SYS_сменить_рабочий_каталог, путь));
}

char *получить_путь_рабочего_каталога(char *буфер_передачи, size_t число_цифр)
{
    long result = __syscall_result(SC2(SYS_получить_путь_рабочего_каталога, буфер_передачи, число_цифр));
    return result < 0 ? (char *)0 : буфер_передачи;
}

int дублировать_ссылку_на_открытый_файл(int дескриптор_файла)
{
    return (int)__syscall_result(SC1(SYS_дублировать_ссылку_на_открытый_файл, дескриптор_файла));
}

int дублировать_ссылку_под_заданным_номером(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_дублировать_ссылку_под_заданным_номером, oldfd, newfd));
}

int согласовать_данные_файла(int дескриптор_файла)
{
    return (int)__syscall_result(SC1(SYS_согласовать_данные_файла, дескриптор_файла));
}

void согласовать_все_данные(void)
{
    SC0(SYS_согласовать_все_данные);
}

int проверить_является_ли_терминалом(int дескриптор_файла)
{
    struct состояние_файла st;
    if (получить_состояние_открытого_файла(дескриптор_файла, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int задать_конец_динамической_памяти(void *address)
{
    long result = SC1(SYS_задать_конец_динамической_памяти, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *сместить_конец_динамической_памяти(int increment)
{
    long current = SC1(SYS_задать_конец_динамической_памяти, 0);
    long requested = current + increment;
    if (increment != 0 && задать_конец_динамической_памяти((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t ждать_указанного_потомка(pid_t pid, int *состояние, int options)
{
    long result;
    do {
        result = SC3(7, pid, состояние, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t ждать_потомка(int *состояние)
{
    return ждать_указанного_потомка(-1, состояние, 0);
}
