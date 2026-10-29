#ifndef alkuperäinen_lanka_verkko_otsikko
#define alkuperäinen_lanka_verkko_otsikko
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Valmistele_lanka_verkko(struct netif *);
void 유선망살피기(struct netif *);
uint32_t lanka_verkko_Tilastotiedot(unsigned);
#endif
