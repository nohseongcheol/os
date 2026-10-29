#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *cadeia_VALOR, void *Endereço);
const char *inet_ntop(int 주소체계, const void *Endereço, char *cadeia_VALOR, socklen_t capacidade_VALOR);
#endif
