#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define seŋondir_ñiiɓirde bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define 통신설정바꾸기 setsockopt
#define 망주소해석하기 inet_pton
#define formaa_laylaytol_ñiiɓirde inet_ntop
#define 망차례짧은수 htons
#define 망차례정수 htonl
#define 장치차례짧은수 ntohs
#define 장치차례정수 ntohl
#endif
