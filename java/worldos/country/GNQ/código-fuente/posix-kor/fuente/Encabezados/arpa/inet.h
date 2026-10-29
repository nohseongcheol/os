#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int esquemaDirección, const char *Cadena, void *dirección);
const char *inet_ntop(int esquemaDirección, const void *dirección, char *Cadena, socklen_t valorCapacidad);
#endif
