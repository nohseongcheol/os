#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ବନ୍ଧନ_ଠିକଣା bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ପରିବର୍ତ୍ତନ_ନେଟ୍_ୱାର୍କ୍_ସେଟିଂସ୍ setsockopt
#define ପାର୍ସ_ନେଟ୍_ୱାର୍କ୍_ଠିକଣା inet_pton
#define ଫର୍ମାଟ୍_ନେଟ୍_ୱାର୍କ୍_ଠିକଣା inet_ntop
#define 망차례짧은수 htons
#define ନେଟ୍_ୱାର୍କ୍_ଇଣ୍ଟିଜର htonl
#define 장치차례짧은수 ntohs
#define ଡିଭାଇସ_କ୍ରମ_ଇଣ୍ଟିଜର ntohl
#endif
