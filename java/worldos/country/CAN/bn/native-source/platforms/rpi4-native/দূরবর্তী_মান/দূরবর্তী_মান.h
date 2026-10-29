#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void প্রস্তুত_করুন_দূরবর্তী(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t বোর্ড_শ্যাডো_করা(uintptr_t,uintptr_t);
uintptr_t বোর্ড_শেষ_করা_দূরবর্তী_আদেশ(uintptr_t);
uintptr_t বোর্ড_দূরবর্তী_অপেক্ষা(uintptr_t);
void 원격화면살피기(void);
int নিয়ন্ত্রণ_দূরবর্তী_ডিসপ্লে(unsigned);
#endif
