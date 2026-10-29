#ifndef natív_vezetékes_hálózat_fejléc
#define natív_vezetékes_hálózat_fejléc
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Előkészítés_vezetékes_hálózat(struct netif *);
void 유선망살피기(struct netif *);
uint32_t vezetékes_hálózat_statisztika(unsigned);
#endif
