#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *сап_маани, void *дарек);
const char *inet_ntop(int 주소체계, const void *дарек, char *сап_маани, socklen_t 용량);
#endif
