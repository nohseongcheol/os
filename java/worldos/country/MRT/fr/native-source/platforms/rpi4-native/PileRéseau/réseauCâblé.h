#ifndef entêteRéseauCâbléNatif
#define entêteRéseauCâbléNatif
#include "lwip/netif.h"
int possèdePériphériqueCâblé(void);
err_t préparerRéseauCâblé(struct netif *);
void inspecterRéseauCâblé(struct netif *);
uint32_t statistiquesRéseauCâblé(unsigned);
#endif
