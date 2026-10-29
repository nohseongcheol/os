#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define жасау_қатысушы socket
#define байланыстыру_мекенжай bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define өзгерту_желі_Параметрлер setsockopt
#define талдау_желі_мекенжай inet_pton
#define пішім_желі_мекенжай inet_ntop
#define 망차례짧은수 htons
#define желі_бүтін_сан htonl
#define 장치차례짧은수 ntohs
#define құрылғы_рет_бүтін_сан ntohl
#endif
