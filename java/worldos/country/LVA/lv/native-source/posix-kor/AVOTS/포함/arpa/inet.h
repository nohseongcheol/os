#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *virkne_VALUE, void *adrese);
const char *inet_ntop(int 주소체계, const void *adrese, char *virkne_VALUE, socklen_t noslodze_VALUE);
#endif
