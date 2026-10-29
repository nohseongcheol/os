#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ھەرپ_تىزمىسى_قىممىتى, void *ئادرېس);
const char *inet_ntop(int 주소체계, const void *ئادرېس, char *ھەرپ_تىزمىسى_قىممىتى, socklen_t 용량);
#endif
