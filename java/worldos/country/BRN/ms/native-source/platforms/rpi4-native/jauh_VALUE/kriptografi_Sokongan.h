#ifndef asal_kriptografi_Pengepala
#define asal_kriptografi_Pengepala
#include <stddef.h>
#include <stdint.h>
void *peruntuk_jauh(size_t);
void keluaran_jauh(void *);
void *원격재할당(void *, size_t);
int jauh_rawak(unsigned char *, unsigned);
void jauh_ringkasan(const void *, size_t, unsigned char [32]);
#endif
