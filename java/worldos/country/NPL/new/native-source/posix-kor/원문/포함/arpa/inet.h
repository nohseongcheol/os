#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *문자열, void *주소);
const char *inet_ntop(int 주소체계, const void *주소, char *문자열, socklen_t 용량);
#endif
