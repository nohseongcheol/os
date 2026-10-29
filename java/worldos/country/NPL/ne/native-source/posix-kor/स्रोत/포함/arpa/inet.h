#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *स्ट्रिङ_मान, void *ठेगाना);
const char *inet_ntop(int 주소체계, const void *ठेगाना, char *स्ट्रिङ_मान, socklen_t 용량);
#endif
