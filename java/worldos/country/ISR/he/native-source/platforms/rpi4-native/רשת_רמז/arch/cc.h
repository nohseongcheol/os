#include "../../명명/기계연결이름.h"
#ifndef מקורי_רשת_מהדר_כותרת
#define מקורי_רשת_מהדר_כותרת
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(קואורדינטת_x) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(קואורדינטת_x) 커널중단(קואורדינטת_x)
#endif
