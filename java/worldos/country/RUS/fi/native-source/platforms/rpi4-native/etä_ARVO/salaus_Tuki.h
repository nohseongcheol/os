#ifndef alkuperäinen_salaus_otsikko
#define alkuperäinen_salaus_otsikko
#include <stddef.h>
#include <stdint.h>
void *jakaa_etä(size_t);
void julkaista_etä(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void etä_yhteenveto(const void *, size_t, unsigned char [32]);
#endif
