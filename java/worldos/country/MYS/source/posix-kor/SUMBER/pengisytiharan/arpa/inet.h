#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *rentetan_VALUE, void *e_mel);
const char *inet_ntop(int 주소체계, const void *e_mel, char *rentetan_VALUE, socklen_t kapasiti_VALUE);
#endif
