#ifndef đầuMụcMạngHữuTuyếnBảnĐịa
#define đầuMụcMạngHữuTuyếnBảnĐịa
#include "lwip/netif.h"
int cóThiếtBịHữuTuyến(void);
err_t chuẩnBịMạngHữuTuyến(struct netif *);
void xemXétMạngHữuTuyến(struct netif *);
uint32_t thốngKêMạngHữuTuyến(unsigned);
#endif
