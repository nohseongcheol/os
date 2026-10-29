#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define বান্ধক_ঠিকনা bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define পৰিবৰ্তন_কৰক_নেটৱৰ্ক_ছেটিংছ setsockopt
#define পাৰ্ছ_কৰক_নেটৱৰ্ক_ঠিকনা inet_pton
#define সজ্জা_নেটৱৰ্ক_ঠিকনা inet_ntop
#define 망차례짧은수 htons
#define নেটৱৰ্ক_পূর্ণ_সংখ্যা htonl
#define 장치차례짧은수 ntohs
#define চেলফোন_ক্ৰম_পূর্ণ_সংখ্যা ntohl
#endif
