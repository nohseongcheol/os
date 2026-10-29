#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *tekenreeks_WAARDE, void *ADRES);
const char *inet_ntop(int 주소체계, const void *ADRES, char *tekenreeks_WAARDE, socklen_t capaciteit_WAARDE);
#endif
