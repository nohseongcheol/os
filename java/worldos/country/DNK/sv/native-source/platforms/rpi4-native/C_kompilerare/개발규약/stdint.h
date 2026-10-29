#ifndef JK_STDINT_H
#define JK_STDINT_H
typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef short int16_t;
typedef unsigned short uint16_t;
typedef int int32_t;
typedef unsigned uint32_t;
typedef long int64_t;
typedef unsigned long uint64_t;
typedef long intptr_t;
typedef unsigned long uintptr_t;
#define UINTPTR_MAX (~(uintptr_t)0)
#define UINT64_MAX (~(uint64_t)0)
#define UINT32_MAX 0xffffffffU
#define INT32_MAX 2147483647
#define INT32_MIN (-2147483647-1)
#define SIZE_MAX UINTPTR_MAX
#endif
