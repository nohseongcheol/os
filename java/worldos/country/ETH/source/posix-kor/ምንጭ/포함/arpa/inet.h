#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ኅብረቁምፊ_እሴት, void *አድራሻ);
const char *inet_ntop(int 주소체계, const void *አድራሻ, char *ኅብረቁምፊ_እሴት, socklen_t 용량);
#endif
