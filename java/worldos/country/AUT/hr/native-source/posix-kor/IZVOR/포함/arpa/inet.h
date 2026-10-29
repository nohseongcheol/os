#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *niz_VALUE, void *adresa);
const char *inet_ntop(int 주소체계, const void *adresa, char *niz_VALUE, socklen_t kapacitet_VALUE);
#endif
