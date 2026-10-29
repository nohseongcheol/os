/* Freestanding byte order only; no host libc socket headers. */
#ifndef natív_bájt_rendelési_fejléc
#define natív_bájt_rendelési_fejléc
#include <stdint.h>
static inline uint32_t htonl(uint32_t ÉRTÉK) { return __builtin_bswap32(ÉRTÉK); }
static inline uint32_t ntohl(uint32_t ÉRTÉK) { return __builtin_bswap32(ÉRTÉK); }
static inline uint16_t htons(uint16_t ÉRTÉK) { return __builtin_bswap16(ÉRTÉK); }
static inline uint16_t ntohs(uint16_t ÉRTÉK) { return __builtin_bswap16(ÉRTÉK); }
#endif
