#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *سلسلة_قيمة, void *عنوان);
const char *inet_ntop(int 주소체계, const void *عنوان, char *سلسلة_قيمة, socklen_t قدرة_قيمة);
#endif
