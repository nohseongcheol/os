#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *สตริง_ค่า, void *อีเมล);
const char *inet_ntop(int 주소체계, const void *อีเมล, char *สตริง_ค่า, socklen_t ความจุ_ค่า);
#endif
