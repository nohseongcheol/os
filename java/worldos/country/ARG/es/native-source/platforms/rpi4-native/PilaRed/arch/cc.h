#include "../../denominación/nombresEnlazarMáquina.h"
#ifndef encabezadoCompiladorRedNativo
#define encabezadoCompiladorRedNativo
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(coordenadaCoordenadaHorizontal) ((void)0)
extern void paradaFatalNúcleo(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(coordenadaCoordenadaHorizontal) paradaFatalNúcleo(coordenadaCoordenadaHorizontal)
#endif
