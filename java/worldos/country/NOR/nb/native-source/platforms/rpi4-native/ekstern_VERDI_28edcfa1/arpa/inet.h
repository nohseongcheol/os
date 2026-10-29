/* Freestanding byte order only; no host libc socket headers. */
#ifndef opprinnelig_byte_ordrehode
#define opprinnelig_byte_ordrehode
#include <stdint.h>
static inline uint32_t htonl(uint32_t VERDI) { return __builtin_bswap32(VERDI); }
static inline uint32_t ntohl(uint32_t VERDI) { return __builtin_bswap32(VERDI); }
static inline uint16_t htons(uint16_t VERDI) { return __builtin_bswap16(VERDI); }
static inline uint16_t ntohs(uint16_t VERDI) { return __builtin_bswap16(VERDI); }
#endif
