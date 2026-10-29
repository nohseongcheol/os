#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define ចង_អ៊ីម៉ែល bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define កែប្រែ_ណិតវឺក_ការកំណត់ setsockopt
#define ញែក_ណិតវឺក_អ៊ីម៉ែល inet_pton
#define ទំរង់_ណិតវឺក_អ៊ីម៉ែល inet_ntop
#define 망차례짧은수 htons
#define ណិតវឺក_ចំនួនគត់ htonl
#define 장치차례짧은수 ntohs
#define ឧបករណ៍_លំដាប់_ចំនួនគត់ ntohl
#endif
