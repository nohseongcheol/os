#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define उपयोगकर्ता_छवि_समाप्त_करें 0x02c00000ul
#define उपयोगकर्ता_ढ़ेर_समाप्त_करें 0x02ed0000ul
#define उपयोगकर्ता_स्टैक_पता 0x02f00000ul
#define उपयोगकर्ता_समाप्त_करें 0x03000000ul
#define 사용자쪽수 ((उपयोगकर्ता_समाप्त_करें - 사용자바탕) / 4096ul)
#define उपयोगकर्ता_निष्पादन_योग्य_फ़ाइल_त्रुटि (-8)
#define उपयोगकर्ता_डेटा_त्रुटि (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t रजिस्टर_डेटा[31], आदेश_पद, अवस्था_कोड, स्टैक_पता; } उपयोगकर्ता_फ़्रेम;
void 사용자체계준비(void);
int उपयोगकर्ता_अपवाद(उपयोगकर्ता_फ़्रेम *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t बोर्ड_उपयोगकर्ता_चलाएँ(uintptr_t);
uintptr_t बोर्ड_उपयोगकर्ता_मान्य_करें(void);
uintptr_t बोर्ड_उपयोगकर्ता_नियंत्रण(uintptr_t);
uint32_t पढें_उपयोगकर्ता_अवस्था(unsigned, unsigned);
#endif
