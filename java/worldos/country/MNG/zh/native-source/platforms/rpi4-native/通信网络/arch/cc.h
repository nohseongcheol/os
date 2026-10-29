#include "../../命名/计算机连接名称列.h"
#ifndef 原生网络编译器头部
#define 原生网络编译器头部
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(横坐标坐标) ((void)0)
extern void 内核致命停止(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(横坐标坐标) 内核致命停止(横坐标坐标)
#endif
