#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ব্যৱহাৰকৰ্তা_ছবি_অন্ত_কৰক 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ব্যৱহাৰকৰ্তা_ষ্টেক_ঠিকনা 0x02f00000ul
#define ব্যৱহাৰকৰ্তা_অন্ত_কৰক 0x03000000ul
#define 사용자쪽수 ((ব্যৱহাৰকৰ্তা_অন্ত_কৰক - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ব্যৱহাৰকৰ্তা_ডাটা_ত্ৰুটি (-1001)
#define 사용자실행오류 (-1002)
#define ব্যৱহাৰকৰ্তা_অবৈধ_নিৰ্দেশনা (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t পঞ্জীয়ন_কৰক_ডাটা[31], আদেশ_স্থান_সলনি_কৰক, 상태값, ষ্টেক_ঠিকনা; } ব্যৱহাৰকৰ্তা_ফ্ৰেম;
void 사용자체계준비(void);
int 사용자예외(ব্যৱহাৰকৰ্তা_ফ্ৰেম *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ব_ৰ্ড_ব্যৱহাৰকৰ্তা_চলন(uintptr_t);
uintptr_t ব_ৰ্ড_ব্যৱহাৰকৰ্তা_বৈধকৰণ_কৰক(void);
uintptr_t ব_ৰ্ড_ব্যৱহাৰকাৰী_নিয়ন্ত্ৰণ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
