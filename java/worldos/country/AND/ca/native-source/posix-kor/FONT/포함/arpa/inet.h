#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *cadena_VALOR, void *Adreça);
const char *inet_ntop(int 주소체계, const void *Adreça, char *cadena_VALOR, socklen_t capacitat_VALOR);
#endif
