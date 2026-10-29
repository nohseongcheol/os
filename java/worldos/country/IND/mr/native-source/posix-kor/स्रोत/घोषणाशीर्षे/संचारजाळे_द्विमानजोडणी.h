#ifndef JKOROS_KOREAN_NETWORK_H
#define JKOROS_KOREAN_NETWORK_H
#include <sys/socket.h>
#include <sys/time.h>
#include <arpa/inet.h>
#define संचारटोक_तयार_करा socket
#define बाइंड_करा_पत्ता bind
#define स्वतंत्रसंदेश_डेटा_पाठवा sendto
#define स्वतंत्रसंदेश_डेटा_स्वीकारा recvfrom
#define संचारद्वार_पत्ता_वाचा getsockname
#define बदल_करा_संचारजाळे_सेटिंग्ज setsockopt
#define संचारजाळे_पत्ता_पार्स_करा inet_pton
#define स्वरूप_संचारजाळे_पत्ता inet_ntop
#define संचारजाळे_लघु htons
#define संचारजाळे_पूर्णांक htonl
#define मोबाइल_क्रम_लघु ntohs
#define मोबाइल_क्रम_पूर्णांक ntohl
#endif
