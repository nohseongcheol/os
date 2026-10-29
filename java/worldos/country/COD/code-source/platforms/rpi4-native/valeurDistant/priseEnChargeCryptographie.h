#ifndef entêteCryptographieNatif
#define entêteCryptographieNatif
#include <stddef.h>
#include <stdint.h>
void *allouerDistant(size_t);
void libérerDistant(void *);
void *réallouerDistant(void *, size_t);
int aléatoireDistant(unsigned char *, unsigned);
void résuméDistant(const void *, size_t, unsigned char [32]);
#endif
