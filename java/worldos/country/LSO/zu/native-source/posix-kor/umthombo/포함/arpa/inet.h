#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *uchunge_inani, void *ikheli);
const char *inet_ntop(int 주소체계, const void *ikheli, char *uchunge_inani, socklen_t 용량);
#endif
