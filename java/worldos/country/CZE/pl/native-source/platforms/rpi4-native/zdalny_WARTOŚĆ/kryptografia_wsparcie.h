#ifndef natywny_kryptografia_Nagłówek
#define natywny_kryptografia_Nagłówek
#include <stddef.h>
#include <stdint.h>
void *przydzielić_zdalny(size_t);
void wersja_zdalny(void *);
void *원격재할당(void *, size_t);
int zdalny_losowy(unsigned char *, unsigned);
void zdalny_podsumowanie(const void *, size_t, unsigned char [32]);
#endif
