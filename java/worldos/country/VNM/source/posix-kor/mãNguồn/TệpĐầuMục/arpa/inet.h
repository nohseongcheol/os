#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int lượcĐồĐịaChỉ, const char *ChuỗiKýTự, void *địaChỉ);
const char *inet_ntop(int lượcĐồĐịaChỉ, const void *địaChỉ, char *ChuỗiKýTự, socklen_t giáTrịSứcChứa);
#endif
