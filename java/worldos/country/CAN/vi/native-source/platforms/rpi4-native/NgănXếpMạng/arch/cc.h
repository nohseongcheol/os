#include "../../cáchĐặtTên/cácTênLiênKếtMáy.h"
#ifndef đầuMụcTrìnhBiênDịchMạngBảnĐịa
#define đầuMụcTrìnhBiênDịchMạngBảnĐịa
#include <stdint.h>
#include <stddef.h>
#define LWIP_NO_INTTYPES_H 1
#define LWIP_NO_CTYPE_H 1
#define LWIP_PLATFORM_DIAG(tọaĐộX) ((void)0)
extern void dừngKhẩnNhân(const char *) __attribute__((noreturn));
#define LWIP_PLATFORM_ASSERT(tọaĐộX) dừngKhẩnNhân(tọaĐộX)
#endif
