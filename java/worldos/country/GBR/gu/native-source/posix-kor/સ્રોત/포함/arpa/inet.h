#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *સ્ટ્રિંગ_મૂલ્ય, void *સરનામું);
const char *inet_ntop(int 주소체계, const void *સરનામું, char *સ્ટ્રિંગ_મૂલ્ય, socklen_t 용량);
#endif
