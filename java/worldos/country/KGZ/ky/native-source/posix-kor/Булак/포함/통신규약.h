#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define байланыштыруу_дарек bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define өзгөртүү_Желе_Орнотуулар setsockopt
#define талдоо_Желе_дарек inet_pton
#define формат_Желе_дарек inet_ntop
#define 망차례짧은수 htons
#define Желе_бүтүн_сан htonl
#define 장치차례짧은수 ntohs
#define түзмөк_ылгоо_ирети_бүтүн_сан ntohl
#endif
