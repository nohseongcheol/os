/* Freestanding byte order only; no host libc socket headers. */
#ifndef nativní_pořadí_bajtů_Nadpis
#define nativní_pořadí_bajtů_Nadpis
#include <stdint.h>
static inline uint32_t htonl(uint32_t HODNOTA) { return __builtin_bswap32(HODNOTA); }
static inline uint32_t ntohl(uint32_t HODNOTA) { return __builtin_bswap32(HODNOTA); }
static inline uint16_t htons(uint16_t HODNOTA) { return __builtin_bswap16(HODNOTA); }
static inline uint16_t ntohs(uint16_t HODNOTA) { return __builtin_bswap16(HODNOTA); }
#endif
