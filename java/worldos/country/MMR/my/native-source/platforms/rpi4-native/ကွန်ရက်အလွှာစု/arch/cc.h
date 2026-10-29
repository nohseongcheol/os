#include "../../명명/စက်ချိတ်အမည်များ.h"
#ifndef ကိုယ်ပိုင်ကွန်ရက်ဘာသာပြန်စက်ခေါင်းစီး
#define ကိုယ်ပိုင်ကွန်ရက်ဘာသာပြန်စက်ခေါင်းစီး
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(xတည်နေရာအမှတ်) ((void)0)
extern void 커널중단(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(xတည်နေရာအမှတ်) 커널중단(xတည်နေရာအမှတ်)
#endif
