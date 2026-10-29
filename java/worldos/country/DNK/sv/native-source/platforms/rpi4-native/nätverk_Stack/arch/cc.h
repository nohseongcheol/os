#include "../../명명/기계연결이름.h"
#ifndef ursprunglig_nätverk_kompilerare_huvud
#define ursprunglig_nätverk_kompilerare_huvud
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(x_koordinat) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(x_koordinat) 커널중단(x_koordinat)
#endif
