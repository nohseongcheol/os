#include "../../명명/기계연결이름.h"
#ifndef собственный_сеть_компилятор_Заголовок
#define собственный_сеть_компилятор_Заголовок
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(координата_X) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(координата_X) 커널중단(координата_X)
#endif
