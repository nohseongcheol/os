#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *स्ट्रिंग_मान, void *पता);
const char *inet_ntop(int 주소체계, const void *पता, char *स्ट्रिंग_मान, socklen_t क्षमता_मान);
#endif
