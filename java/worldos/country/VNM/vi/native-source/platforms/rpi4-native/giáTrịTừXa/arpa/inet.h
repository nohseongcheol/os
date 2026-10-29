/* Freestanding byte order only; no host libc socket headers. */
#ifndef đầuMụcThứTựByteBảnĐịa
#define đầuMụcThứTựByteBảnĐịa
#include <stdint.h>
static inline uint32_t htonl(uint32_t giáTrị) { return __builtin_bswap32(giáTrị); }
static inline uint32_t ntohl(uint32_t giáTrị) { return __builtin_bswap32(giáTrị); }
static inline uint16_t htons(uint16_t giáTrị) { return __builtin_bswap16(giáTrị); }
static inline uint16_t ntohs(uint16_t giáTrị) { return __builtin_bswap16(giáTrị); }
#endif
