/* Freestanding byte order only; no host libc socket headers. */
#ifndef systemnahByteReihenfolgeKopf
#define systemnahByteReihenfolgeKopf
#include <stdint.h>
static inline uint32_t htonl(uint32_t Wert) { return __builtin_bswap32(Wert); }
static inline uint32_t ntohl(uint32_t Wert) { return __builtin_bswap32(Wert); }
static inline uint16_t htons(uint16_t Wert) { return __builtin_bswap16(Wert); }
static inline uint16_t ntohs(uint16_t Wert) { return __builtin_bswap16(Wert); }
#endif
