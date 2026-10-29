#include "../../명명/기계연결이름.h"
#ifndef 자체통신번역기머리
#define 자체통신번역기머리
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(x_ସଂଯୋଜନ) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(x_ସଂଯୋଜନ) 커널중단(x_ସଂଯୋଜନ)
#endif
