#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *низ_стойност, void *адрес);
const char *inet_ntop(int 주소체계, const void *адрес, char *низ_стойност, socklen_t капацитет_стойност);
#endif
