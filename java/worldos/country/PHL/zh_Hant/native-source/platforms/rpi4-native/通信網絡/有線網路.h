#ifndef 原生有線網路標頭
#define 原生有線網路標頭
#include "lwip/netif.h"
int 擁有有線設備(void);
err_t 準備有線網路(struct netif *);
void 審查有線網路(struct netif *);
uint32_t 有線網路統計(unsigned);
#endif
