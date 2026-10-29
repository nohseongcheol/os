#ifndef 자체유선망머리
#define 자체유선망머리
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Pregătiți_cu_fir_rețea(struct netif *);
void 유선망살피기(struct netif *);
uint32_t cu_fir_rețea_Statistică(unsigned);
#endif
