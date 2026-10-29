#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *स्ट्रिंग_मोल, void *नामो);
const char *inet_ntop(int 주소체계, const void *नामो, char *स्ट्रिंग_मोल, socklen_t 용량);
#endif
