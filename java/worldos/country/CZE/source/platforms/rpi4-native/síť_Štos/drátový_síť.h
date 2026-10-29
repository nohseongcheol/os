#ifndef nativní_drátový_síť_Nadpis
#define nativní_drátový_síť_Nadpis
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Připravit_drátový_síť(struct netif *);
void 유선망살피기(struct netif *);
uint32_t drátový_síť_Statistika(unsigned);
#endif
