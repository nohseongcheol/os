#ifndef oprindelig_traditionel_netværk_Header
#define oprindelig_traditionel_netværk_Header
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Tilrettelæg_traditionel_netværk(struct netif *);
void 유선망살피기(struct netif *);
uint32_t traditionel_netværk_Statistik(unsigned);
#endif
