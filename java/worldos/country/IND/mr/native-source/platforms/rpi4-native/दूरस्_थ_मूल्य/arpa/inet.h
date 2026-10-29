/* Freestanding byte order only; no host libc socket headers. */
#ifndef स्वकीय_बाइट_क्रम_शीर्षलेख
#define स्वकीय_बाइट_क्रम_शीर्षलेख
#include <stdint.h>
static inline uint32_t htonl(uint32_t मूल्य) { return __builtin_bswap32(मूल्य); }
static inline uint32_t ntohl(uint32_t मूल्य) { return __builtin_bswap32(मूल्य); }
static inline uint16_t htons(uint16_t मूल्य) { return __builtin_bswap16(मूल्य); }
static inline uint16_t ntohs(uint16_t मूल्य) { return __builtin_bswap16(मूल्य); }
#endif
