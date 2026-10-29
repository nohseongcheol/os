/* Freestanding byte order only; no host libc socket headers. */
#ifndef εγγενής_σειρά_byte_κεφαλίδα
#define εγγενής_σειρά_byte_κεφαλίδα
#include <stdint.h>
static inline uint32_t htonl(uint32_t τιμή) { return __builtin_bswap32(τιμή); }
static inline uint32_t ntohl(uint32_t τιμή) { return __builtin_bswap32(τιμή); }
static inline uint16_t htons(uint16_t τιμή) { return __builtin_bswap16(τιμή); }
static inline uint16_t ntohs(uint16_t τιμή) { return __builtin_bswap16(τιμή); }
#endif
