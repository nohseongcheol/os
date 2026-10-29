#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *низа_VALUE_6ca8363c, void *адреса);
const char *inet_ntop(int 주소체계, const void *адреса, char *низа_VALUE_6ca8363c, socklen_t 용량);
#endif
