#ifndef 자체유선망머리
#define 자체유선망머리
#include "lwip/netif.h"
int 유선장치있음(void);
err_t প্ৰস্তুত_কৰক_তাঁৰযুক্ত_নেটৱৰ্ক(struct netif *);
void 유선망살피기(struct netif *);
uint32_t 유선망집계(unsigned);
#endif
