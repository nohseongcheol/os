/* Freestanding byte order only; no host libc socket headers. */
#ifndef מקורי_סדר_בתים_כותרת
#define מקורי_סדר_בתים_כותרת
#include <stdint.h>
static inline uint32_t htonl(uint32_t ערך) { return __builtin_bswap32(ערך); }
static inline uint32_t ntohl(uint32_t ערך) { return __builtin_bswap32(ערך); }
static inline uint16_t htons(uint16_t ערך) { return __builtin_bswap16(ערך); }
static inline uint16_t ntohs(uint16_t ערך) { return __builtin_bswap16(ערך); }
#endif
