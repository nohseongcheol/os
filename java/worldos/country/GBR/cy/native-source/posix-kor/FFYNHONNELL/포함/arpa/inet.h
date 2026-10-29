#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *testun_VALUE, void *ADDRESS);
const char *inet_ntop(int 주소체계, const void *ADDRESS, char *testun_VALUE, socklen_t 용량);
#endif
