#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *מחרוזת_ערך, void *למען);
const char *inet_ntop(int 주소체계, const void *למען, char *מחרוזת_ערך, socklen_t קיבולת_ערך);
#endif
