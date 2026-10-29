#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int पत्ता_योजना, const char *स्ट्रींग_मूल्य, void *पत्ता);
const char *inet_ntop(int पत्ता_योजना, const void *पत्ता, char *स्ट्रींग_मूल्य, socklen_t धारणक्षमता_मूल्य);
#endif
