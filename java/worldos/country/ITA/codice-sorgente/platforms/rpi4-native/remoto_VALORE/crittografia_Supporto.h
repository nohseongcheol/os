#ifndef nativo_crittografia_Intestazione
#define nativo_crittografia_Intestazione
#include <stddef.h>
#include <stdint.h>
void *allocare_remoto(size_t);
void release_remoto(void *);
void *원격재할당(void *, size_t);
int remoto_casuale(unsigned char *, unsigned);
void remoto_riepilogo(const void *, size_t, unsigned char [32]);
#endif
