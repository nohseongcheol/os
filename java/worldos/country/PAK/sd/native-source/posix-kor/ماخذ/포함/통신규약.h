#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ٻڌو_پتو bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define تبديل_ڪريو_نيٽ_ورڪ_سيٽنگون setsockopt
#define 망주소해석하기 inet_pton
#define وضع_نيٽ_ورڪ_پتو inet_ntop
#define 망차례짧은수 htons
#define نيٽ_ورڪ_عدد_صحيح htonl
#define 장치차례짧은수 ntohs
#define آلو_ترتيب_عدد_صحيح ntohl
#endif
