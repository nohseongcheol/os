#ifndef opprinnelig_kryptografi_Topptekst
#define opprinnelig_kryptografi_Topptekst
#include <stddef.h>
#include <stdint.h>
void *tildele_ekstern(size_t);
void frigi_ekstern(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void ekstern_sammendrag(const void *, size_t, unsigned char [32]);
#endif
