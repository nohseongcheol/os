#include "../../명명/기계연결이름.h"
#ifndef 자체통신번역기머리
#define 자체통신번역기머리
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(rëddu_iks_yi) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(rëddu_iks_yi) 커널중단(rëddu_iks_yi)
#endif
