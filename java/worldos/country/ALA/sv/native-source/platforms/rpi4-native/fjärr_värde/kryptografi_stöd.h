#ifndef ursprunglig_kryptografi_huvud
#define ursprunglig_kryptografi_huvud
#include <stddef.h>
#include <stdint.h>
void *allokera_fjärr(size_t);
void släppa_fjärr(void *);
void *원격재할당(void *, size_t);
int fjärr_slumpmässig(unsigned char *, unsigned);
void fjärr_sammanfattning(const void *, size_t, unsigned char [32]);
#endif
