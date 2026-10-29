#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, void *ଠିକଣା);
const char *inet_ntop(int 주소체계, const void *ଠିକଣା, char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ, socklen_t 용량);
#endif
