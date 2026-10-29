#ifndef natív_kriptográfia_fejléc
#define natív_kriptográfia_fejléc
#include <stddef.h>
#include <stdint.h>
void *kioszt_távoli(size_t);
void kiad_távoli(void *);
void *원격재할당(void *, size_t);
int távoli_véletlenszerű(unsigned char *, unsigned);
void távoli_összegzés(const void *, size_t, unsigned char [32]);
#endif
