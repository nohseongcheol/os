#ifndef 原生有线网络头部
#define 原生有线网络头部
#include "lwip/netif.h"
int 拥有有线设备(void);
err_t 准备有线网络(struct netif *);
void 审查有线网络(struct netif *);
uint32_t 有线网络统计(unsigned);
#endif
