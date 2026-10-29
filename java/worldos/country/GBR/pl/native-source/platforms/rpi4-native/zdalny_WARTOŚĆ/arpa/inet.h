/* Freestanding byte order only; no host libc socket headers. */
#ifndef natywny_kolejność_bajtów_Nagłówek
#define natywny_kolejność_bajtów_Nagłówek
#include <stdint.h>
static inline uint32_t htonl(uint32_t WARTOŚĆ) { return __builtin_bswap32(WARTOŚĆ); }
static inline uint32_t ntohl(uint32_t WARTOŚĆ) { return __builtin_bswap32(WARTOŚĆ); }
static inline uint16_t htons(uint16_t WARTOŚĆ) { return __builtin_bswap16(WARTOŚĆ); }
static inline uint16_t ntohs(uint16_t WARTOŚĆ) { return __builtin_bswap16(WARTOŚĆ); }
#endif
