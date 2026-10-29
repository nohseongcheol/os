#ifndef nativeWiredNetworkHeader
#define nativeWiredNetworkHeader
#include "lwip/netif.h"
int hasWiredDevice(void);
err_t prepareWiredNetwork(struct netif *);
void inspectWiredNetwork(struct netif *);
uint32_t wiredNetworkStatistics(unsigned);
#endif
