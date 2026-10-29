#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *အဝေးနေရာခွဲဝေ(size_t);
void အဝေးလွှတ်ပေး(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void အဝေးအကျဉ်းချုပ်(const void *, size_t, unsigned char [32]);
#endif
