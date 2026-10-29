#ifndef JKOROS_INET_H
#define JKOROS_INET_H
#include <netinet/in.h>
#define INET_ADDRSTRLEN 16
int inet_pton(int လိပ်စာအစီအစဉ်, const char *အက္ခရာစဉ်, void *လိပ်စာ);
const char *inet_ntop(int လိပ်စာအစီအစဉ်, const void *လိပ်စာ, char *အက္ခရာစဉ်, socklen_t ဆံ့ပမာဏ);
#endif
