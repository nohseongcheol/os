#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Create_участник socket
#define BIND_АДРЕС bind
#define написать_датаграмма_данные sendto
#define получить_датаграмма_данные recvfrom
#define чтение_сокет_АДРЕС getsockname
#define изменить_сеть_Настройки setsockopt
#define анализировать_идентификатор_сети inet_pton
#define формат_идентификатор_сети inet_ntop
#define 망차례짧은수 htons
#define сеть_целое_число htonl
#define 장치차례짧은수 ntohs
#define устройство_заказ_целое_число ntohl
#endif
