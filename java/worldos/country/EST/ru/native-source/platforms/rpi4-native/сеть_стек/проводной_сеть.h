#ifndef собственный_проводной_сеть_Заголовок
#define собственный_проводной_сеть_Заголовок
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Подготовить_проводной_сеть(struct netif *);
void 유선망살피기(struct netif *);
uint32_t проводной_сеть_Статистика(unsigned);
#endif
