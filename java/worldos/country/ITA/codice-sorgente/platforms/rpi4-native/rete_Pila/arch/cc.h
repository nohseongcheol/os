#include "../../명명/기계연결이름.h"
#ifndef nativo_rete_compilatore_Intestazione
#define nativo_rete_compilatore_Intestazione
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(coordinata_x) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(coordinata_x) 커널중단(coordinata_x)
#endif
