#ifndef oprindelig_kryptografi_Header
#define oprindelig_kryptografi_Header
#include <stddef.h>
#include <stdint.h>
void *tildel_fjern(size_t);
void udgive_fjern(void *);
void *원격재할당(void *, size_t);
int fjern_vilkårlig(unsigned char *, unsigned);
void fjern_resume(const void *, size_t, unsigned char [32]);
#endif
