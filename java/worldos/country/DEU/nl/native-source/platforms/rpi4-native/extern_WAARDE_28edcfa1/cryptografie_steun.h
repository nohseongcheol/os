#ifndef systeemeigen_cryptografie_header
#define systeemeigen_cryptografie_header
#include <stddef.h>
#include <stdint.h>
void *toewijzen_extern(size_t);
void versie_extern(void *);
void *원격재할당(void *, size_t);
int extern_willekeurig(unsigned char *, unsigned);
void extern_samenvatting(const void *, size_t, unsigned char [32]);
#endif
