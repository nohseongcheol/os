#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define Създаване_участник socket
#define обвързвам_адрес bind
#define изпращам_дейтаграма_данни sendto
#define получавам_дейтаграма_данни recvfrom
#define 통신주소읽기 getsockname
#define променям_мрежа_Настройки setsockopt
#define анализирам_мрежов_идентификатор inet_pton
#define формат_мрежов_идентификатор inet_ntop
#define 망차례짧은수 htons
#define мрежа_цяло_число htonl
#define 장치차례짧은수 ntohs
#define устройство_ред_цяло_число ntohl
#endif
