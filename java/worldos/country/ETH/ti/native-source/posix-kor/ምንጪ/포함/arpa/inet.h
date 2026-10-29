#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ሕብረ_ቁምፊ_ዋጋ, void *ኣድራሻ);
const char *inet_ntop(int 주소체계, const void *ኣድራሻ, char *ሕብረ_ቁምፊ_ዋጋ, socklen_t 용량);
#endif
