#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *строка_ЗНАЧЕН, void *АДРЕС);
const char *inet_ntop(int 주소체계, const void *АДРЕС, char *строка_ЗНАЧЕН, socklen_t емкость_ЗНАЧЕН);
#endif
