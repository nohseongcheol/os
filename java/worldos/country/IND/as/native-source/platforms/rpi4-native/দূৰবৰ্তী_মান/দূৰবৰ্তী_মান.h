#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void প্ৰস্তুত_কৰক_দূৰবৰ্তী(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t ব_ৰ্ড_ছাঁয়াকৰণ(uintptr_t,uintptr_t);
uintptr_t ব_ৰ্ড_অন্ত_কৰক_দূৰবৰ্তী_আদেশ(uintptr_t);
uintptr_t 보드원격대기(uintptr_t);
void 원격화면살피기(void);
int নিয়ন্ত্রণ_দূৰবৰ্তী_প্রদর্শন(unsigned);
#endif
