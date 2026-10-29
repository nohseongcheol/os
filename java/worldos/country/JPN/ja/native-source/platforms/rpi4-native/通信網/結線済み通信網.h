#ifndef 自前結線済み通信網ヘッダー
#define 自前結線済み通信網ヘッダー
#include "lwip/netif.h"
int 保有結線済み装置(void);
err_t 結線済み通信網用意(struct netif *);
void 結線済み通信網調査(struct netif *);
uint32_t 結線済み通信網統計(unsigned);
#endif
