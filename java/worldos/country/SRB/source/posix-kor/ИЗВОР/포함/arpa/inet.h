#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ниска_вриједност, void *адреса);
const char *inet_ntop(int 주소체계, const void *адреса, char *ниска_вриједност, socklen_t капацитет_вриједност);
#endif
