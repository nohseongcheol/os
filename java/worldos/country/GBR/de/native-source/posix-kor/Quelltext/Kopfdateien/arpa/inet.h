#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int adresseSchema, const char *Zeichenkette, void *adresse);
const char *inet_ntop(int adresseSchema, const void *adresse, char *Zeichenkette, socklen_t kapazitätWert);
#endif
