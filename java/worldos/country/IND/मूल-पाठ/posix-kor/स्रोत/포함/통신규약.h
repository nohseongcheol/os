#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define बनाएँ_एंडपॉइंट socket
#define बाइंड_करें_पता bind
#define 자료전문보내기 sendto
#define 자료전문받기 recvfrom
#define पढें_सॉकेट_पता getsockname
#define परिवर्तित_करें_नेटवर्क_सेटिंग setsockopt
#define पार्स_करें_नेटवर्क_पता inet_pton
#define फॉर्मैट_नेटवर्क_पता inet_ntop
#define 망차례짧은수 htons
#define नेटवर्क_पूर्णांक htonl
#define 장치차례짧은수 ntohs
#define उपकरण_क्रम_पूर्णांक ntohl
#endif
