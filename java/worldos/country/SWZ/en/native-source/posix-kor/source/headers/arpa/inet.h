#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int addressScheme, const char *stringValue, void *address);
const char *inet_ntop(int addressScheme, const void *address, char *stringValue, socklen_t capacityValue);
#endif
