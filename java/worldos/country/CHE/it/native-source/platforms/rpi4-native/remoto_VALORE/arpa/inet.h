/* Freestanding byte order only; no host libc socket headers. */
#ifndef nativo_ordine_dei_byte_Intestazione
#define nativo_ordine_dei_byte_Intestazione
#include <stdint.h>
static inline uint32_t htonl(uint32_t VALORE) { return __builtin_bswap32(VALORE); }
static inline uint32_t ntohl(uint32_t VALORE) { return __builtin_bswap32(VALORE); }
static inline uint16_t htons(uint16_t VALORE) { return __builtin_bswap16(VALORE); }
static inline uint16_t ntohs(uint16_t VALORE) { return __builtin_bswap16(VALORE); }
#endif
