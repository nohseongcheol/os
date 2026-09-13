#ifndef _include_система_socket
#define _include_система_socket

#include <основные_определения.h>
#include <система/типы_данных.h>

typedef unsigned short тип_семейства_адресов;

struct адрес_конечной_точки_связи {
    тип_семейства_адресов семейство_адресов_конечной_точки;
    char данные_адреса[14];
};

#define семейство_адресов_не_задано 0
#define код_семейства_межсетевых_адресов 2
#define семейство_межсетевых_протоколов код_семейства_межсетевых_адресов

#define конечная_точка_потока_данных 1
#define конечная_точка_датаграмм 2

#define остановить_приём 0
#define остановить_передачу 1
#define остановить_оба_направления 2

#ifdef __cplusplus
extern "C" {
#endif
int создать_оконечную_точку_связи(int domain, int type, int protocol);
int привязать_местный_адрес(int дескриптор_файла, const struct адрес_конечной_точки_связи *address, тип_длины_адреса address_len);
int соединить_с_другой_стороной(int дескриптор_файла, const struct адрес_конечной_точки_связи *address, тип_длины_адреса address_len);
int подготовить_приём_соединений(int дескриптор_файла, int backlog);
int принять_соединение(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *address_len);
int получить_местный_адрес_точки(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *address_len);
int получить_адрес_другой_стороны(int дескриптор_файла, struct адрес_конечной_точки_связи *address, тип_длины_адреса *address_len);
ssize_t отправить(int дескриптор_файла, const void *буфер_передачи_2, size_t длина, int flags);
ssize_t получить(int дескриптор_файла, void *буфер_передачи_2, size_t длина, int flags);
ssize_t отправить_по_адресу(int дескриптор_файла, const void *message, size_t длина, int flags,
               const struct адрес_конечной_точки_связи *dest_addr, тип_длины_адреса dest_len);
ssize_t получить_с_адресом_отправителя(int дескриптор_файла, void *буфер_передачи_2, size_t длина, int flags,
                 struct адрес_конечной_точки_связи *address, тип_длины_адреса *address_len);
int закрыть_направление_связи(int дескриптор_файла, int how);
int задать_настройку_точки_связи(int дескриптор_файла, int level, int option_name,
               const void *option_value, тип_длины_адреса option_len);
#ifdef __cplusplus
}
#endif

#endif
