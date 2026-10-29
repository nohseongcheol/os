#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *stringa_VALORE, void *e_mail);
const char *inet_ntop(int 주소체계, const void *e_mail, char *stringa_VALORE, socklen_t capacità_VALORE);
#endif
