#ifndef opprinnelig_kabelbasert_nettverk_Topptekst
#define opprinnelig_kabelbasert_nettverk_Topptekst
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Forbered_kabelbasert_nettverk(struct netif *);
void 유선망살피기(struct netif *);
uint32_t kabelbasert_nettverk_statistikk(unsigned);
#endif
