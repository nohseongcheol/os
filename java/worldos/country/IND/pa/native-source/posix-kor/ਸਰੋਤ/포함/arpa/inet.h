#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, void *ਪਤਾ);
const char *inet_ntop(int 주소체계, const void *ਪਤਾ, char *ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ, socklen_t 용량);
#endif
