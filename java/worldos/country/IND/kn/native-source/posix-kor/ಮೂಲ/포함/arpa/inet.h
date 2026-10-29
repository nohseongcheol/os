#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, void *ಇಮೇಲ್);
const char *inet_ntop(int 주소체계, const void *ಇಮೇಲ್, char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ, socklen_t 용량);
#endif
