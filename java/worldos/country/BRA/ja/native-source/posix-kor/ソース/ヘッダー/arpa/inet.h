#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 番地方式体系, const char *文字列, void *番地);
const char *inet_ntop(int 番地方式体系, const void *番地, char *文字列, socklen_t 容積値);
#endif
