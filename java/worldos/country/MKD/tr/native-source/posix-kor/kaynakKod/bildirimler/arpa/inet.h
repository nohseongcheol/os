#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *dize_değer, void *ADRES);
const char *inet_ntop(int 주소체계, const void *ADRES, char *dize_değer, socklen_t kapasite_değer);
#endif
