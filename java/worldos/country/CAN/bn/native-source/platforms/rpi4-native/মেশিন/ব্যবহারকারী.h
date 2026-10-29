#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ব্যবহারকারী_ছবি_শেষ_করা 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ব্যবহারকারী_গাদা_ইমেইল 0x02f00000ul
#define ব্যবহারকারী_শেষ_করা 0x03000000ul
#define 사용자쪽수 ((ব্যবহারকারী_শেষ_করা - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ব্যবহারকারী_ডাটা_ত্রুটি (-1001)
#define 사용자실행오류 (-1002)
#define ব্যবহারকারী_অবৈধ_নির্দেশ (-1003)
#define ব্যবহারকারী_টাইমআউট (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t নিবন্ধন_করুন_ডাটা[31], আদেশ_পদ, অবস্হা_কোড, গাদা_ইমেইল; } ব্যবহারকারী_ফ্রেম;
void 사용자체계준비(void);
int ব্যবহারকারী_ব্যতিক্রম(ব্যবহারকারী_ফ্রেম *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t বোর্ড_ব্যবহারকারী_রান(uintptr_t);
uintptr_t বোর্ড_ব্যবহারকারী_বৈধ_করুন(void);
uintptr_t বোর্ড_ব্যবহারকারীর_নিয়ন্ত্রণ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
