#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define उपेगकर्तो_BASE 0x02000000ul
#define उपेगकर्तो_IMAGE_सोपोवचें 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define उपेगकर्तो_स्टॅक_नामो 0x02f00000ul
#define उपेगकर्तो_सोपोवचें 0x03000000ul
#define उपेगकर्तो_पान_COUNT ((उपेगकर्तो_सोपोवचें - उपेगकर्तो_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define उपेगकर्तो_डेटा_चूक (-1001)
#define 사용자실행오류 (-1002)
#define उपेगकर्तो_अवैध_समजावणी (-1003)
#define उपेगकर्तो_कालबाह्य (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t नोंदणी_डेटा[31], आदेश_स्थिती, स्थिती_CODE, स्टॅक_नामो; } उपेगकर्तो_फ्रेम;
void 사용자체계준비(void);
int 사용자예외(उपेगकर्तो_फ्रेम *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t बोर्ड_उपेगकर्तो_चलोवप(uintptr_t);
uintptr_t बोर्ड_उपेगकर्तो_पुनर्तपासणी_करची(void);
uintptr_t बोर्ड_उपेगकर्तो_नियंत्रण(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
