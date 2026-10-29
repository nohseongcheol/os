#include "../../命名/計算機連接名稱列.h"
#ifndef 原生網路編譯器標頭
#define 原生網路編譯器標頭
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(橫座標座標) ((void)0)
extern void 內核致命停止(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(橫座標座標) 內核致命停止(橫座標座標)
#endif
