/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <преобразование_адресов/порядок_байтов.h>
#include <система/syscall.h>
#include <система/socket.h>

enum { SYS_socketcall = 102 };
enum {
    SC_создать_оконечную_точку_связи = 1, SC_привязать_местный_адрес = 2, SC_соединить_с_другой_стороной = 3, SC_подготовить_приём_соединений = 4,
    SC_принять_соединение = 5, SC_получить_местный_адрес_точки = 6, SC_получить_адрес_другой_стороны = 7,
    SC_отправить = 9, SC_получить = 10, SC_отправить_по_адресу = 11, SC_получить_с_адресом_отправителя = 12,
    SC_закрыть_направление_связи = 13, SC_задать_настройку_точки_связи = 14
};

static long socket_call(long call, unsigned long *аргументы)
{
    return __syscall_result(
        __syscall6(SYS_socketcall, call, (long)аргументы, 0, 0, 0, 0));
}

uint16_t перевести_16_разрядов_в_сетевой_порядок(uint16_t значение) { return (uint16_t)((значение << 8) | (значение >> 8)); }
uint16_t перевести_16_разрядов_в_машинный_порядок(uint16_t значение) { return перевести_16_разрядов_в_сетевой_порядок(значение); }
uint32_t перевести_32_разряда_в_сетевой_порядок(uint32_t значение)
{
    return ((значение & 0x000000ffU) << 24) | ((значение & 0x0000ff00U) << 8) |
           ((значение & 0x00ff0000U) >> 8) | ((значение & 0xff000000U) >> 24);
}
uint32_t перевести_32_разряда_в_машинный_порядок(uint32_t значение) { return перевести_32_разряда_в_сетевой_порядок(значение); }

int создать_оконечную_точку_связи(int domain, int type, int protocol)
{
    unsigned long a[3] = {(unsigned long)domain, (unsigned long)type, (unsigned long)protocol};
    return (int)socket_call(SC_создать_оконечную_точку_связи, a);
}

int привязать_местный_адрес(int дескриптор_файла, const struct адрес_конечной_точки_связи *address, тип_длины_адреса длина)
{
    unsigned long a[3] = {(unsigned long)дескриптор_файла, (unsigned long)address, длина};
    return (int)socket_call(SC_привязать_местный_адрес, a);
}

int соединить_с_другой_стороной(int дескриптор_файла, const struct адрес_конечной_точки_связи *address, тип_длины_адреса длина)
{
    unsigned long a[3] = {(unsigned long)дескриптор_файла, (unsigned long)address, длина};
    return (int)socket_call(SC_соединить_с_другой_стороной, a);
}

int подготовить_приём_соединений(int дескриптор_файла, int backlog)
{
    unsigned long a[2] = {(unsigned long)дескриптор_файла, (unsigned long)backlog};
    return (int)socket_call(SC_подготовить_приём_соединений, a);
}

int принять_соединение(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *длина)
{
    unsigned long a[3] = {(unsigned long)дескриптор_файла, (unsigned long)address, (unsigned long)длина};
    return (int)socket_call(SC_принять_соединение, a);
}

int получить_местный_адрес_точки(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *длина)
{
    unsigned long a[3] = {(unsigned long)дескриптор_файла, (unsigned long)address, (unsigned long)длина};
    return (int)socket_call(SC_получить_местный_адрес_точки, a);
}

int получить_адрес_другой_стороны(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *длина)
{
    unsigned long a[3] = {(unsigned long)дескриптор_файла, (unsigned long)address, (unsigned long)длина};
    return (int)socket_call(SC_получить_адрес_другой_стороны, a);
}

ssize_t отправить(int дескриптор_файла, const void *буфер_передачи_2, size_t длина, int flags)
{
    unsigned long a[4] = {(unsigned long)дескриптор_файла, (unsigned long)буфер_передачи_2, длина, (unsigned long)flags};
    return (ssize_t)socket_call(SC_отправить, a);
}

ssize_t получить(int дескриптор_файла, void *буфер_передачи_2, size_t длина, int flags)
{
    unsigned long a[4] = {(unsigned long)дескриптор_файла, (unsigned long)буфер_передачи_2, длина, (unsigned long)flags};
    return (ssize_t)socket_call(SC_получить, a);
}

ssize_t отправить_по_адресу(int дескриптор_файла, const void *буфер_передачи_2, size_t длина, int flags,
               const struct адрес_конечной_точки_связи *address, тип_длины_адреса address_length)
{
    unsigned long a[6] = {(unsigned long)дескриптор_файла, (unsigned long)буфер_передачи_2, длина,
                          (unsigned long)flags, (unsigned long)address, address_length};
    return (ssize_t)socket_call(SC_отправить_по_адресу, a);
}

ssize_t получить_с_адресом_отправителя(int дескриптор_файла, void *буфер_передачи_2, size_t длина, int flags,
                 struct адрес_конечной_точки_связи *address, тип_длины_адреса *address_length)
{
    unsigned long a[6] = {(unsigned long)дескриптор_файла, (unsigned long)буфер_передачи_2, длина,
                          (unsigned long)flags, (unsigned long)address,
                          (unsigned long)address_length};
    return (ssize_t)socket_call(SC_получить_с_адресом_отправителя, a);
}

int закрыть_направление_связи(int дескриптор_файла, int how)
{
    unsigned long a[2] = {(unsigned long)дескриптор_файла, (unsigned long)how};
    return (int)socket_call(SC_закрыть_направление_связи, a);
}

int задать_настройку_точки_связи(int дескриптор_файла, int level, int option_name,
               const void *option_value, тип_длины_адреса option_len)
{
    unsigned long a[5] = {(unsigned long)дескриптор_файла, (unsigned long)level,
                          (unsigned long)option_name, (unsigned long)option_value,
                          option_len};
    return (int)socket_call(SC_задать_настройку_точки_связи, a);
}
