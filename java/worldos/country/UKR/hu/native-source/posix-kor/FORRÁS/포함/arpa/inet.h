#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *sztring_ÉRTÉK, void *CÍM);
const char *inet_ntop(int 주소체계, const void *CÍM, char *sztring_ÉRTÉK, socklen_t kapacitás_ÉRTÉK);
#endif
