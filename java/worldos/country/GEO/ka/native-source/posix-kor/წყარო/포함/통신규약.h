#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define მიბმა_მისამართი bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define შეცვლა_ქსელი_პარამეტრები setsockopt
#define ანალიზი_ქსელი_მისამართი inet_pton
#define ფორმატი_ქსელი_მისამართი inet_ntop
#define 망차례짧은수 htons
#define ქსელი_მთელი_რიცხვი htonl
#define 장치차례짧은수 ntohs
#define მობილური_დახარისხების_თანმიმდევრობა_მთელი_რიცხვი ntohl
#endif
