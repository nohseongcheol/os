#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *అక్షరసరం_మూల్యం, void *ఇమెయిల్);
const char *inet_ntop(int 주소체계, const void *ఇమెయిల్, char *అక్షరసరం_మూల్యం, socklen_t 용량);
#endif
