/* Freestanding byte order only; no host libc socket headers. */
#ifndef أصلي_ترتيب_البايت_عنوان
#define أصلي_ترتيب_البايت_عنوان
#include <stdint.h>
static inline uint32_t htonl(uint32_t قيمة) { return __builtin_bswap32(قيمة); }
static inline uint32_t ntohl(uint32_t قيمة) { return __builtin_bswap32(قيمة); }
static inline uint16_t htons(uint16_t قيمة) { return __builtin_bswap16(قيمة); }
static inline uint16_t ntohs(uint16_t قيمة) { return __builtin_bswap16(قيمة); }
#endif
