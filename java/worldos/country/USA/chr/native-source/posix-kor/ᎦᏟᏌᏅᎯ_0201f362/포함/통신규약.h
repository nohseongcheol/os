#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define BIND_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define ᎯᏁᏟᏴᎾ_ᏧᎾᏚᏓᎵ_ᏕᎦᎧᎲᎢ setsockopt
#define 망주소해석하기 inet_pton
#define ᏱᎬᏁᎸᎯ_ᏧᎾᏚᏓᎵ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ inet_ntop
#define 망차례짧은수 htons
#define ᏧᎾᏚᏓᎵ_integer htonl
#define 장치차례짧은수 ntohs
#define ᎠᏂᎩᏍᎩ_ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_integer ntohl
#endif
