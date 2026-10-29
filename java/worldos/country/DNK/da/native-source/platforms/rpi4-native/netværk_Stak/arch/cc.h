#include "../../명명/기계연결이름.h"
#ifndef oprindelig_netværk_compiler_Header
#define oprindelig_netværk_compiler_Header
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(X_koordinat) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(X_koordinat) 커널중단(X_koordinat)
#endif
