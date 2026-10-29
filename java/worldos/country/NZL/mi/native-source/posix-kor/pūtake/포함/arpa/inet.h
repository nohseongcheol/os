#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *aho_uara, void *ADDRESS);
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *aho_uara, socklen_t 용량);
#endif
