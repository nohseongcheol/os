#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define बाँध्नु_ठेगाना bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define परिवर्तन_सञ्जाल_सेटिङहरू setsockopt
#define पदच्छेद_गर्नुहोस्_सञ्जाल_ठेगाना inet_pton
#define ढाँचा_सञ्जाल_ठेगाना inet_ntop
#define 망차례짧은수 htons
#define सञ्जाल_पूर्ण_सङ्ख्या htonl
#define 장치차례짧은수 ntohs
#define मोबाइल_अर्डर_पूर्ण_सङ्ख्या ntohl
#endif
