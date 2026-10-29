#ifndef systemnahVerdrahtetNetzwerkKopf
#define systemnahVerdrahtetNetzwerkKopf
#include "lwip/netif.h"
int hatVerdrahtetGerät(void);
err_t verdrahtetNetzwerkVorbereiten(struct netif *);
void verdrahtetNetzwerkUntersuchen(struct netif *);
uint32_t verdrahtetNetzwerkStatistik(unsigned);
#endif
