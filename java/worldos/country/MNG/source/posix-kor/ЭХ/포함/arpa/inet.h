#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *мөр_утга_6ca8363c, void *хаяг);
const char *inet_ntop(int 주소체계, const void *хаяг, char *мөр_утга_6ca8363c, socklen_t 용량);
#endif
