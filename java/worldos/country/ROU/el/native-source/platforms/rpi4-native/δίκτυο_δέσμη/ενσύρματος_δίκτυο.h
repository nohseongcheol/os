#ifndef εγγενής_ενσύρματος_δίκτυο_κεφαλίδα
#define εγγενής_ενσύρματος_δίκτυο_κεφαλίδα
#include "lwip/netif.h"
int 유선장치있음(void);
err_t Προετοίμασε_ενσύρματος_δίκτυο(struct netif *);
void 유선망살피기(struct netif *);
uint32_t ενσύρματος_δίκτυο_Στατιστικά(unsigned);
#endif
