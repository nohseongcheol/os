#ifndef systeemeigen_bekabeld_net_header
#define systeemeigen_bekabeld_net_header
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Bereid_voor_bekabeld_net(struct netif *);
void 유선망살피기(struct netif *);
uint32_t bekabeld_net_Statistieken(unsigned);
#endif
