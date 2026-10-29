#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define አጣምር_አድራሻ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ለውጥ_መረብ_ቅንብሮች setsockopt
#define ተንትን_መረብ_አድራሻ inet_pton
#define ቅርጸት_መረብ_አድራሻ inet_ntop
#define 망차례짧은수 htons
#define መረብ_ኢንተጀር htonl
#define 장치차례짧은수 ntohs
#define መሳሪያ_ቅደም_ተከተል_ኢንተጀር ntohl
#endif
