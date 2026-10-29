#ifndef encabezadoPaqueteNativo
#define encabezadoPaqueteNativo
#include <stddef.h>
int abrirJAR(const char *nombreEntradaElementoArchivo);
int leerJAR(const char *nombre, unsigned char *datosResultado, unsigned capacidadBúfer);
const char *principalJAR(void);
#endif
