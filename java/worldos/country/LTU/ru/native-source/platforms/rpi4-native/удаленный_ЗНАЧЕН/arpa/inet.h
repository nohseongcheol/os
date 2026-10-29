/* Freestanding byte order only; no host libc socket headers. */
#ifndef собственный_порядок_байтов_Заголовок
#define собственный_порядок_байтов_Заголовок
#include <stdint.h>
static inline uint32_t htonl(uint32_t ЗНАЧЕН) { return __builtin_bswap32(ЗНАЧЕН); }
static inline uint32_t ntohl(uint32_t ЗНАЧЕН) { return __builtin_bswap32(ЗНАЧЕН); }
static inline uint16_t htons(uint16_t ЗНАЧЕН) { return __builtin_bswap16(ЗНАЧЕН); }
static inline uint16_t ntohs(uint16_t ЗНАЧЕН) { return __builtin_bswap16(ЗНАЧЕН); }
#endif
