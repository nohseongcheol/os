#ifndef yerel_kablolu_ağ_Başlık
#define yerel_kablolu_ağ_Başlık
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Hazırlan_kablolu_ağ(struct netif *);
void 유선망살피기(struct netif *);
uint32_t kablolu_ağ_İstatistik(unsigned);
#endif
