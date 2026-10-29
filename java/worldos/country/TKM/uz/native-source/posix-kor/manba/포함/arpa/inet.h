#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *satr_VALUE, void *manzil);
const char *inet_ntop(int 주소체계, const void *manzil, char *satr_VALUE, socklen_t 용량);
#endif
