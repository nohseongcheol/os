#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *სტრიქონი_მნიშვნელობა, void *მისამართი);
const char *inet_ntop(int 주소체계, const void *მისამართი, char *სტრიქონი_მნიშვნელობა, socklen_t 용량);
#endif
