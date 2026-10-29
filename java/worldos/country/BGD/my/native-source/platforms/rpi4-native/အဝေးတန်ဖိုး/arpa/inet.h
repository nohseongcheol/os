/* Freestanding byte order only; no host libc socket headers. */
#ifndef ကိုယ်ပိုင်ဘိုက်အစဉ်ခေါင်းစီး
#define ကိုယ်ပိုင်ဘိုက်အစဉ်ခေါင်းစီး
#include <stdint.h>
static inline uint32_t htonl(uint32_t တန်ဖိုး) { return __builtin_bswap32(တန်ဖိုး); }
static inline uint32_t ntohl(uint32_t တန်ဖိုး) { return __builtin_bswap32(တန်ဖိုး); }
static inline uint16_t htons(uint16_t တန်ဖိုး) { return __builtin_bswap16(တန်ဖိုး); }
static inline uint16_t ntohs(uint16_t တန်ဖိုး) { return __builtin_bswap16(တန်ဖိုး); }
#endif
