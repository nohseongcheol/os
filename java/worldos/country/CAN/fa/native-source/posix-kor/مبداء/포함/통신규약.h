#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define مرتبط_سازی_آدرس bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define تغییر_شبکه_تنظیمات setsockopt
#define تفسیر_شبکه_آدرس inet_pton
#define قالب_شبکه_آدرس inet_ntop
#define 망차례짧은수 htons
#define شبکه_عدد_صحیح htonl
#define 장치차례짧은수 ntohs
#define دستگاه_ترتیب_عدد_صحیح ntohl
#endif
