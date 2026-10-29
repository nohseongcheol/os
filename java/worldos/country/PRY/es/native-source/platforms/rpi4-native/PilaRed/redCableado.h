#ifndef encabezadoRedCableadoNativo
#define encabezadoRedCableadoNativo
#include "lwip/netif.h"
int tieneDispositivoCableado(void);
err_t prepararRedCableado(struct netif *);
void inspeccionarRedCableado(struct netif *);
uint32_t estadísticasRedCableado(unsigned);
#endif
