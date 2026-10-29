#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ADDRESS bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define atharraich_lìonra_roghainnean setsockopt
#define 망주소해석하기 inet_pton
#define fòrmat_lìonra_ADDRESS inet_ntop
#define 망차례짧은수 htons
#define lìonra_àireamh_shlàn htonl
#define 장치차례짧은수 ntohs
#define uidheam_òrdugh_àireamh_shlàn ntohl
#endif
