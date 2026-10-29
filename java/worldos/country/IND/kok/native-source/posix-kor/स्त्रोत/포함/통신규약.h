#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_नामो bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define बदलचें_नॅटवर्क_मांडावळी setsockopt
#define व्याकरणी_फोडणिशी_नॅटवर्क_नामो inet_pton
#define स्वरूप_नॅटवर्क_नामो inet_ntop
#define 망차례짧은수 htons
#define नॅटवर्क_पुर्णांक htonl
#define 장치차례짧은수 ntohs
#define मोबायल_क्रम_पुर्णांक ntohl
#endif
