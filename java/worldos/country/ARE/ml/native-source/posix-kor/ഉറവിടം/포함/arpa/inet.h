#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *സ്ട്രിംഗ്_മൂല്യം, void *ഇമെയിൽ);
const char *inet_ntop(int 주소체계, const void *ഇമെയിൽ, char *സ്ട്രിംഗ്_മൂല്യം, socklen_t 용량);
#endif
