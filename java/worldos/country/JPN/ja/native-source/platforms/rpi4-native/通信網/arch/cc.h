#include "../../命名/機械連結名前一覧.h"
#ifndef 自前通信網コンパイラヘッダー
#define 自前通信網コンパイラヘッダー
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(横座標) ((void)0)
extern void 中核致命停止(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(横座標) 中核致命停止(横座標)
#endif
