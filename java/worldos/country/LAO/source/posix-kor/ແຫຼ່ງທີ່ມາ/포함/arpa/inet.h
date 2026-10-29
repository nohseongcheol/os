#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *ສະຕຣິງ_ຄ່າ, void *ອີເມວ);
const char *inet_ntop(int 주소체계, const void *ອີເມວ, char *ສະຕຣິງ_ຄ່າ, socklen_t 용량);
#endif
