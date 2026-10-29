#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *අනුලකුණු_වැල_අගය, void *යොමුව);
const char *inet_ntop(int 주소체계, const void *යොමුව, char *අනුලකුණු_වැල_අගය, socklen_t 용량);
#endif
