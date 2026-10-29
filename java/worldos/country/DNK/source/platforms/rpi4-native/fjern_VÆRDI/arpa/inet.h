/* Freestanding byte order only; no host libc socket headers. */
#ifndef oprindelig_byte_ordrehoved
#define oprindelig_byte_ordrehoved
#include <stdint.h>
static inline uint32_t htonl(uint32_t VÆRDI) { return __builtin_bswap32(VÆRDI); }
static inline uint32_t ntohl(uint32_t VÆRDI) { return __builtin_bswap32(VÆRDI); }
static inline uint16_t htons(uint16_t VÆRDI) { return __builtin_bswap16(VÆRDI); }
static inline uint16_t ntohs(uint16_t VÆRDI) { return __builtin_bswap16(VÆRDI); }
#endif
