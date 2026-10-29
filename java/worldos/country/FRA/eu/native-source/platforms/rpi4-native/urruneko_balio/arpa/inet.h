/* Freestanding byte order only; no host libc socket headers. */
#ifndef 자체바이트순서머리
#define 자체바이트순서머리
#include <stdint.h>
static inline uint32_t htonl(uint32_t balio) { return __builtin_bswap32(balio); }
static inline uint32_t ntohl(uint32_t balio) { return __builtin_bswap32(balio); }
static inline uint16_t htons(uint16_t balio) { return __builtin_bswap16(balio); }
static inline uint16_t ntohs(uint16_t balio) { return __builtin_bswap16(balio); }
#endif
