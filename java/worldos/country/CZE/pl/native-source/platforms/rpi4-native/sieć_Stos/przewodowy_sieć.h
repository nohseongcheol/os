#ifndef natywny_przewodowy_sieć_Nagłówek
#define natywny_przewodowy_sieć_Nagłówek
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Przygotuj_przewodowy_sieć(struct netif *);
void 유선망살피기(struct netif *);
uint32_t przewodowy_sieć_Statystyka(unsigned);
#endif
