#include "../../명명/기계연결이름.h"
#ifndef nativo_rede_compilador_Cabeçalho
#define nativo_rede_compilador_Cabeçalho
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(coordenada_X) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(coordenada_X) 커널중단(coordenada_X)
#endif
