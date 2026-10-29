#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *Zeechefolleg_VALUE, void *Adress);
const char *inet_ntop(int 주소체계, const void *Adress, char *Zeechefolleg_VALUE, socklen_t 용량);
#endif
