#ifndef nativo_cablato_rete_Intestazione
#define nativo_cablato_rete_Intestazione
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Prepara_cablato_rete(struct netif *);
void 유선망살피기(struct netif *);
uint32_t cablato_rete_Statistiche(unsigned);
#endif
