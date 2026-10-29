#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *eilutė_VALUE, void *ADDRESS);
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *eilutė_VALUE, socklen_t pajėgumas_VALUE);
#endif
