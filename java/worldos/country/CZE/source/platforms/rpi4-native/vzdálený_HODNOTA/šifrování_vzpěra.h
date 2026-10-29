#ifndef nativní_šifrování_Nadpis
#define nativní_šifrování_Nadpis
#include <stddef.h>
#include <stdint.h>
void *přidělit_vzdálený(size_t);
void verze_vzdálený(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void vzdálený_souhrn(const void *, size_t, unsigned char [32]);
#endif
