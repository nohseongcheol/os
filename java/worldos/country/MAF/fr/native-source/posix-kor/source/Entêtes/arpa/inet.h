#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int schémaAdresse, const char *Chaîne, void *adresse);
const char *inet_ntop(int schémaAdresse, const void *adresse, char *Chaîne, socklen_t valeurCapacité);
#endif
