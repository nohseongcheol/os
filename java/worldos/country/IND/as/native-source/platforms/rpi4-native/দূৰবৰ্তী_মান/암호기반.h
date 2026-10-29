#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *আৱণ্টন_দূৰবৰ্তী(size_t);
void ৰিলিজ_দূৰবৰ্তী(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void দূৰবৰ্তী_সাৰাংশ(const void *, size_t, unsigned char [32]);
#endif
