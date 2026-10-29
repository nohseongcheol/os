#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *niz_VALUE, void *naslov);
const char *inet_ntop(int 주소체계, const void *naslov, char *niz_VALUE, socklen_t zmogljivost_VALUE);
#endif
