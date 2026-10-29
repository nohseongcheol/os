#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *tungo_thamani, void *anwani);
const char *inet_ntop(int 주소체계, const void *anwani, char *tungo_thamani, socklen_t 용량);
#endif
