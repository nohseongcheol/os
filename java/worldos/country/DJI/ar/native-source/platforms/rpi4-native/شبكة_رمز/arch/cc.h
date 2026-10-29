#include "../../명명/기계연결이름.h"
#ifndef أصلي_شبكة_محول_برمجي_عنوان
#define أصلي_شبكة_محول_برمجي_عنوان
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(الإحداثي_س) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(الإحداثي_س) 커널중단(الإحداثي_س)
#endif
