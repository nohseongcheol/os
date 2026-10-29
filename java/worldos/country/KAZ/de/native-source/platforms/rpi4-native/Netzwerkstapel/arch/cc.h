#include "../../benennung/maschineBindenNamen.h"
#ifndef systemnahNetzwerkÜbersetzerKopf
#define systemnahNetzwerkÜbersetzerKopf
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(waagerechteKoordinateKoordinate) ((void)0)
extern void betriebskernNotstopp(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(waagerechteKoordinateKoordinate) betriebskernNotstopp(waagerechteKoordinateKoordinate)
#endif
