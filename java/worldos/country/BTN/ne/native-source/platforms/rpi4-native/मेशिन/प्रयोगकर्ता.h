#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define प्रयोगकर्ता_छवि_समाप्त_गर्नुहोस् 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define प्रयोगकर्ता_चाङ_ठेगाना 0x02f00000ul
#define प्रयोगकर्ता_समाप्त_गर्नुहोस् 0x03000000ul
#define 사용자쪽수 ((प्रयोगकर्ता_समाप्त_गर्नुहोस् - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define प्रयोगकर्ता_लगत_त्रुटि (-1001)
#define 사용자실행오류 (-1002)
#define प्रयोगकर्ता_अवैधानिक_निर्देशन (-1003)
#define प्रयोगकर्ता_समय_सकियो (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t दर्ता_लगत[31], आदेश_राख्नुहोस्, 상태값, चाङ_ठेगाना; } प्रयोगकर्ता_फ्रेम;
void 사용자체계준비(void);
int 사용자예외(प्रयोगकर्ता_फ्रेम *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t बोर्ड_प्रयोगकर्ता_चलाउनुहोस्(uintptr_t);
uintptr_t बोर्ड_प्रयोगकर्ता_वैध_गर्नुहोस्(void);
uintptr_t बोर्ड_प्रयोगकर्ताको_नियन्त्रण(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
