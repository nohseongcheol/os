#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int 주소체계, const char *συμβολοσειρά_τιμή, void *διεύθυνση);
const char *inet_ntop(int 주소체계, const void *διεύθυνση, char *συμβολοσειρά_τιμή, socklen_t Δυνατότητα_τιμή);
#endif
