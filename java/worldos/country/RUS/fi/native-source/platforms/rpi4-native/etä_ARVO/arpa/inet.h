/* Freestanding byte order only; no host libc socket headers. */
#ifndef alkuperäinen_tavu_tilausotsikko
#define alkuperäinen_tavu_tilausotsikko
#include <stdint.h>
static inline uint32_t htonl(uint32_t ARVO) { return __builtin_bswap32(ARVO); }
static inline uint32_t ntohl(uint32_t ARVO) { return __builtin_bswap32(ARVO); }
static inline uint16_t htons(uint16_t ARVO) { return __builtin_bswap16(ARVO); }
static inline uint16_t ntohs(uint16_t ARVO) { return __builtin_bswap16(ARVO); }
#endif
