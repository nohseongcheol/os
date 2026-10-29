#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 地址方案, const char *字符串, void *地址);
const char *inet_ntop(int 地址方案, const void *地址, char *字符串, socklen_t 容量值);
#endif
