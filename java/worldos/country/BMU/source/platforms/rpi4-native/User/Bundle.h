#ifndef nativeBundleHeader
#define nativeBundleHeader
#include <stddef.h>
int jarOpen(const char *fileEntryName);
int jarRead(const char *name, unsigned char *resultData, unsigned bufferCapacity);
const char *jarMain(void);
#endif
