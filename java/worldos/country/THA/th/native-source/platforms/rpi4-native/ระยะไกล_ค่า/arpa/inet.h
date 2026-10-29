/* Freestanding byte order only; no host libc socket headers. */
#ifndef ดั้งเดิม_ลําดับไบต์_ส่วนหัว
#define ดั้งเดิม_ลําดับไบต์_ส่วนหัว
#include <stdint.h>
static inline uint32_t htonl(uint32_t ค่า) { return __builtin_bswap32(ค่า); }
static inline uint32_t ntohl(uint32_t ค่า) { return __builtin_bswap32(ค่า); }
static inline uint16_t htons(uint16_t ค่า) { return __builtin_bswap16(ค่า); }
static inline uint16_t ntohs(uint16_t ค่า) { return __builtin_bswap16(ค่า); }
#endif
