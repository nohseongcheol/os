#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *տող_արժեք_6ca8363c, void *հասցե);
const char *inet_ntop(int 주소체계, const void *հասցե, char *տող_արժեք_6ca8363c, socklen_t 용량);
#endif
