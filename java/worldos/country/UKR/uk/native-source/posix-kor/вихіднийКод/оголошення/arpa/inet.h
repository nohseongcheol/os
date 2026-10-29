#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *рядок_значення, void *Адреса);
const char *inet_ntop(int 주소체계, const void *Адреса, char *рядок_значення, socklen_t ресурс_значення_e6ac1362);
#endif
