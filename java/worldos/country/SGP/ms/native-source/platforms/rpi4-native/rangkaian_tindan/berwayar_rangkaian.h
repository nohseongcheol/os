#ifndef asal_berwayar_rangkaian_Pengepala
#define asal_berwayar_rangkaian_Pengepala
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Sediakan_berwayar_rangkaian(struct netif *);
void 유선망살피기(struct netif *);
uint32_t 유선망집계(unsigned);
#endif
