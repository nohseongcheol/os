/* Freestanding byte order only; no host libc socket headers. */
#ifndef encabezadoOrdenByteNativo
#define encabezadoOrdenByteNativo
#include <stdint.h>
static inline uint32_t htonl(uint32_t valor) { return __builtin_bswap32(valor); }
static inline uint32_t ntohl(uint32_t valor) { return __builtin_bswap32(valor); }
static inline uint16_t htons(uint16_t valor) { return __builtin_bswap16(valor); }
static inline uint16_t ntohs(uint16_t valor) { return __builtin_bswap16(valor); }
#endif
