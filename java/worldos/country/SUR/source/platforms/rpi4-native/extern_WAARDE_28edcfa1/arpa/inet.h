/* Freestanding byte order only; no host libc socket headers. */
#ifndef systeemeigen_byte_orderkop
#define systeemeigen_byte_orderkop
#include <stdint.h>
static inline uint32_t htonl(uint32_t WAARDE) { return __builtin_bswap32(WAARDE); }
static inline uint32_t ntohl(uint32_t WAARDE) { return __builtin_bswap32(WAARDE); }
static inline uint16_t htons(uint16_t WAARDE) { return __builtin_bswap16(WAARDE); }
static inline uint16_t ntohs(uint16_t WAARDE) { return __builtin_bswap16(WAARDE); }
#endif
