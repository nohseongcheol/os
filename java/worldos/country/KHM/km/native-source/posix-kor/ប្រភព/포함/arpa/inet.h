#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *សំនុំអក្សរ_តំលៃ, void *អ៊ីម៉ែល);
const char *inet_ntop(int 주소체계, const void *អ៊ីម៉ែល, char *សំនុំអក្សរ_តំលៃ, socklen_t 용량);
#endif
