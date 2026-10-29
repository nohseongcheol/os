#ifndef מקורי_קווי_רשת_כותרת
#define מקורי_קווי_רשת_כותרת
#include "lwip/netif.h"
int 유선장치있음(void);
err_t להכין_קווי_רשת(struct netif *);
void 유선망살피기(struct netif *);
uint32_t 유선망집계(unsigned);
#endif
