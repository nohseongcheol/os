#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *merkkijono_ARVO, void *OSOITE);
const char *inet_ntop(int 주소체계, const void *OSOITE, char *merkkijono_ARVO, socklen_t kapasiteetti_ARVO);
#endif
