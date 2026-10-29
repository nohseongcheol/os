#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *سلک_قدر, void *پتہ);
const char *inet_ntop(int 주소체계, const void *پتہ, char *سلک_قدر, socklen_t 용량);
#endif
