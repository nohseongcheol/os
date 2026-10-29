/* Freestanding byte order only; no host libc socket headers. */
#ifndef 原生字节排序头部
#define 原生字节排序头部
#include <stdint.h>
static inline uint32_t htonl(uint32_t 值) { return __builtin_bswap32(值); }
static inline uint32_t ntohl(uint32_t 值) { return __builtin_bswap32(值); }
static inline uint16_t htons(uint16_t 值) { return __builtin_bswap16(值); }
static inline uint16_t ntohs(uint16_t 值) { return __builtin_bswap16(值); }
#endif
