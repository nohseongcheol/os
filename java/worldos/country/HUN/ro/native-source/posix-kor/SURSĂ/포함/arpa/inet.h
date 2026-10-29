#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *șir_VALUE, void *adresa);
const char *inet_ntop(int 주소체계, const void *adresa, char *șir_VALUE, socklen_t capacitate_VALUE);
#endif
