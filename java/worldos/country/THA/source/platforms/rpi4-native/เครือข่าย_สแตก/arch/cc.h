#include "../../명명/기계연결이름.h"
#ifndef ดั้งเดิม_เครือข่าย_คอมไพเลอร์_ส่วนหัว
#define ดั้งเดิม_เครือข่าย_คอมไพเลอร์_ส่วนหัว
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(พิกัดแกน_x) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(พิกัดแกน_x) 커널중단(พิกัดแกน_x)
#endif
