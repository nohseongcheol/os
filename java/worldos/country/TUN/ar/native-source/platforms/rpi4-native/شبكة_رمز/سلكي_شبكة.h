#ifndef أصلي_سلكي_شبكة_عنوان
#define أصلي_سلكي_شبكة_عنوان
#include "lwip/netif.h"
int 유선장치있음(void);
err_t إعداد_سلكي_شبكة(struct netif *);
void 유선망살피기(struct netif *);
uint32_t 유선망집계(unsigned);
#endif
