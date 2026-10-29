#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ciąg_WARTOŚĆ, void *Adres);
const char *inet_ntop(int 주소체계, const void *Adres, char *ciąg_WARTOŚĆ, socklen_t pojemność_WARTOŚĆ);
#endif
