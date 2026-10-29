#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *fọ́nrán_iye, void *àdírẹ́ẹ̀sì);
const char *inet_ntop(int 주소체계, const void *àdírẹ́ẹ̀sì, char *fọ́nrán_iye, socklen_t 용량);
#endif
