#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define 통신종단점만들기 socket
#define బైండ్_చేయి_ఇమెయిల్ bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define 통신주소읽기 getsockname
#define మార్చు_నెట్_వర్క్_సెట్టింగ్_లు setsockopt
#define పార్స్_నెట్_వర్క్_ఇమెయిల్ inet_pton
#define ఆకృతి_నెట్_వర్క్_ఇమెయిల్ inet_ntop
#define 망차례짧은수 htons
#define నెట్_వర్క్_పూర్ణాంకం htonl
#define 장치차례짧은수 ntohs
#define పరికరం_క్రమం_పూర్ణాంకం ntohl
#endif
