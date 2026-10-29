/* Freestanding byte order only; no host libc socket headers. */
#ifndef 自前バイト順序ヘッダー
#define 自前バイト順序ヘッダー
#include <stdint.h>
static inline uint32_t htonl(uint32_t 値) { return __builtin_bswap32(値); }
static inline uint32_t ntohl(uint32_t 値) { return __builtin_bswap32(値); }
static inline uint16_t htons(uint16_t 値) { return __builtin_bswap16(値); }
static inline uint16_t ntohs(uint16_t 値) { return __builtin_bswap16(値); }
#endif
