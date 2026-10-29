#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ઉપયોગકર્તા_છબી_અંત_કરો 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ઉપયોગકર્તા_સ્ટેક_સરનામું 0x02f00000ul
#define ઉપયોગકર્તા_અંત_કરો 0x03000000ul
#define 사용자쪽수 ((ઉપયોગકર્તા_અંત_કરો - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ઉપયોગકર્તા_ડેટા_ભૂલ (-1001)
#define 사용자실행오류 (-1002)
#define ઉપયોગકર્તા_અમાન્ય_સૂચના (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t રજિસ્ટર_કરો_ડેટા[31], આદેશ_સ્થિતિ, 상태값, સ્ટેક_સરનામું; } ઉપયોગકર્તા_ફ્રેમ;
void 사용자체계준비(void);
int 사용자예외(ઉપયોગકર્તા_ફ્રેમ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t બોર્ડ_ઉપયોગકર્તા_ચલાવો(uintptr_t);
uintptr_t બોર્ડ_ઉપયોગકર્તા_માન્ય_કરો(void);
uintptr_t બોર્ડ_ઉપયોગકર્તા_નિયંત્રણ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
