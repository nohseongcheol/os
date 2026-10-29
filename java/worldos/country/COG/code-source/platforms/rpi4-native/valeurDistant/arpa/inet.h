/* Freestanding byte order only; no host libc socket headers. */
#ifndef entêteOrdreOctetNatif
#define entêteOrdreOctetNatif
#include <stdint.h>
static inline uint32_t htonl(uint32_t valeur) { return __builtin_bswap32(valeur); }
static inline uint32_t ntohl(uint32_t valeur) { return __builtin_bswap32(valeur); }
static inline uint16_t htons(uint16_t valeur) { return __builtin_bswap16(valeur); }
static inline uint16_t ntohs(uint16_t valeur) { return __builtin_bswap16(valeur); }
#endif
