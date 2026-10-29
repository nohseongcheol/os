#ifndef nativeCryptographyHeader
#define nativeCryptographyHeader
#include <stddef.h>
#include <stdint.h>
void *allocateRemote(size_t);
void releaseRemote(void *);
void *reallocateRemote(void *, size_t);
int remoteRandom(unsigned char *, unsigned);
void remoteSummary(const void *, size_t, unsigned char [32]);
#endif
