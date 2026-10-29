#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *cadea_VALOR, void *ENDEREZO);
const char *inet_ntop(int 주소체계, const void *ENDEREZO, char *cadea_VALOR, socklen_t capacidade_VALOR);
#endif
