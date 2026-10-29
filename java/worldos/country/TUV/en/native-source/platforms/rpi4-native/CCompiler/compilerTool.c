/* Disable host-JIT entry points; this guest compiler writes freestanding ELF. */
#define ONE_SOURCE 1
#include "tcc.h"
#undef TCC_IS_NATIVE
#include "libtcc.c"
