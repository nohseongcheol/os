#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Створення_учасник socket
#define зв_язувати_адреса bind
#define надсилати_дейтаграма_дані sendto
#define отримувати_дейтаграма_дані recvfrom
#define 통신주소읽기 getsockname
#define змінювати_мережа_Настройки setsockopt
#define аналізувати_ідентифікатор_мережі inet_pton
#define формат_ідентифікатор_мережі inet_ntop
#define 망차례짧은수 htons
#define мережа_ціле_число htonl
#define 장치차례짧은수 ntohs
#define пристрій_порядок_ціле_число ntohl
#endif
