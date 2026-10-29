#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *رست_نرخ, void *ناونیشان);
const char *inet_ntop(int 주소체계, const void *ناونیشان, char *رست_نرخ, socklen_t 용량);
#endif
