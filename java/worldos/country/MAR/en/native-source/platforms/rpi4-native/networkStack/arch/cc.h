#include "../../naming/machineLinkNames.h"
#ifndef nativeNetworkCompilerHeader
#define nativeNetworkCompilerHeader
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(xCoordinate) ((void)0)
extern void kernelPanic(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(xCoordinate) kernelPanic(xCoordinate)
#endif
