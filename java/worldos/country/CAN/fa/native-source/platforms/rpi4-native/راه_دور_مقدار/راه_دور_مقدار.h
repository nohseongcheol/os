#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void آماده_کردن_راه_دور(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t تخته_ای_کنترل_از_راه_دور(uintptr_t,uintptr_t);
uintptr_t تخته_ای_پایان_دادن_راه_دور_فرمان(uintptr_t);
uintptr_t تخته_ای_راه_دور_منتظر_ماندن(uintptr_t);
void 원격화면살피기(void);
int کنترل_راه_دور_صفحه_نمایش(unsigned);
#endif
