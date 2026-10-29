#ifndef nativo_com_fio_rede_Cabeçalho
#define nativo_com_fio_rede_Cabeçalho
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Preparar_com_fio_rede(struct netif *);
void 유선망살피기(struct netif *);
uint32_t com_fio_rede_Estatísticas(unsigned);
#endif
