#include "../../명명/기계연결이름.h"
#ifndef natywny_sieć_kompilator_Nagłówek
#define natywny_sieć_kompilator_Nagłówek
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(współrzędna_X) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(współrzędna_X) 커널중단(współrzędna_X)
#endif
