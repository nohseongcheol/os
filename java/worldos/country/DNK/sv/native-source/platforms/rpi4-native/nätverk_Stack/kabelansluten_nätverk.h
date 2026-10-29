#ifndef ursprunglig_kabelansluten_nätverk_huvud
#define ursprunglig_kabelansluten_nätverk_huvud
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Förbereda_kabelansluten_nätverk(struct netif *);
void 유선망살피기(struct netif *);
uint32_t kabelansluten_nätverk_Statistik(unsigned);
#endif
