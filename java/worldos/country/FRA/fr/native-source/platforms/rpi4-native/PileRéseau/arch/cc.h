#include "../../nommage/nomsLierMachine.h"
#ifndef entêteCompilateurRéseauNatif
#define entêteCompilateurRéseauNatif
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(coordonnéeCoordonnéeHorizontale) ((void)0)
extern void arrêtFatalNoyau(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(coordonnéeCoordonnéeHorizontale) arrêtFatalNoyau(coordonnéeCoordonnéeHorizontale)
#endif
