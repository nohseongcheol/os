#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *বন্টন_করা_দূরবর্তী(size_t);
void রিলিজ_দূরবর্তী(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void দূরবর্তী_সামারি(const void *, size_t, unsigned char [32]);
#endif
