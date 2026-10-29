#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *string_VALUE, void *surel);
const char *inet_ntop(int 주소체계, const void *surel, char *string_VALUE, socklen_t kapasitas_VALUE);
#endif
