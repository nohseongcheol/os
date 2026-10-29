/* Freestanding byte order only; no host libc socket headers. */
#ifndef yerel_bayt_sırası_Başlık
#define yerel_bayt_sırası_Başlık
#include <stdint.h>
static inline uint32_t htonl(uint32_t değer) { return __builtin_bswap32(değer); }
static inline uint32_t ntohl(uint32_t değer) { return __builtin_bswap32(değer); }
static inline uint16_t htons(uint16_t değer) { return __builtin_bswap16(değer); }
static inline uint16_t ntohs(uint16_t değer) { return __builtin_bswap16(değer); }
#endif
