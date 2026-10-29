#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *ବଣ୍ଟନ_ଦୂରବର୍ତ୍ତୀ(size_t);
void ରିଲିଜ୍_ଦୂରବର୍ତ୍ତୀ(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void ଦୂରବର୍ତ୍ତୀ_ସାରାଂଶ(const void *, size_t, unsigned char [32]);
#endif
