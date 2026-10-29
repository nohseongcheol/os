#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *řetězec_HODNOTA, void *Adresa);
const char *inet_ntop(int 주소체계, const void *Adresa, char *řetězec_HODNOTA, socklen_t kapacita_HODNOTA);
#endif
