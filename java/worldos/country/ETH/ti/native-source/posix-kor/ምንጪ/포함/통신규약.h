#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ኣጣምር_ኣድራሻ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ለውጥ_ማሕበራዊ_ኔትወርክ_ኣቀማምጣታት setsockopt
#define 망주소해석하기 inet_pton
#define ቅረጽ_ማሕበራዊ_ኔትወርክ_ኣድራሻ inet_ntop
#define 망차례짧은수 htons
#define ማሕበራዊ_ኔትወርክ_ኢንቲጀር htonl
#define 장치차례짧은수 ntohs
#define መሳርሒ_ተርታ_ኢንቲጀር ntohl
#endif
