/* Freestanding byte order only; no host libc socket headers. */
#ifndef 原生位元組排序標頭
#define 原生位元組排序標頭
#include <stdint.h>
static inline uint32_t htonl(uint32_t 值) { return __builtin_bswap32(值); }
static inline uint32_t ntohl(uint32_t 值) { return __builtin_bswap32(值); }
static inline uint16_t htons(uint16_t 值) { return __builtin_bswap16(值); }
static inline uint16_t ntohs(uint16_t 值) { return __builtin_bswap16(值); }
#endif
