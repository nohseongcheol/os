#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ùsòròokwū_valuu, void *àdreèsì);
const char *inet_ntop(int 주소체계, const void *àdreèsì, char *ùsòròokwū_valuu, socklen_t 용량);
#endif
