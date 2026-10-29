#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define বন্ধন_করা_ইমেইল bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define পরিবর্তন_করা_নেটওয়ার্ক_সেটিংস setsockopt
#define বিভাজন_করা_নেটওয়ার্ক_ইমেইল inet_pton
#define বিন্যাস_নেটওয়ার্ক_ইমেইল inet_ntop
#define 망차례짧은수 htons
#define নেটওয়ার্ক_পূর্ণসংখ্যা htonl
#define 장치차례짧은수 ntohs
#define ডিভাইস_ক্রম_পূর্ণসংখ্যা ntohl
#endif
