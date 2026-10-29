/* Freestanding byte order only; no host libc socket headers. */
#ifndef asal_tertib_bait_Pengepala
#define asal_tertib_bait_Pengepala
#include <stdint.h>
static inline uint32_t htonl(uint32_t VALUE) { return __builtin_bswap32(VALUE); }
static inline uint32_t ntohl(uint32_t VALUE) { return __builtin_bswap32(VALUE); }
static inline uint16_t htons(uint16_t VALUE) { return __builtin_bswap16(VALUE); }
static inline uint16_t ntohs(uint16_t VALUE) { return __builtin_bswap16(VALUE); }
#endif
