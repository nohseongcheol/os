/* Freestanding byte order only; no host libc socket headers. */
#ifndef ursprunglig_byte_orderhuvud
#define ursprunglig_byte_orderhuvud
#include <stdint.h>
static inline uint32_t htonl(uint32_t värde) { return __builtin_bswap32(värde); }
static inline uint32_t ntohl(uint32_t värde) { return __builtin_bswap32(värde); }
static inline uint16_t htons(uint16_t värde) { return __builtin_bswap16(värde); }
static inline uint16_t ntohs(uint16_t värde) { return __builtin_bswap16(värde); }
#endif
