#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ئىشلەتكۈچى_رەسىم_تاماملىماق 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ئىشلەتكۈچى_دۆۋە_ئادرېس 0x02f00000ul
#define ئىشلەتكۈچى_تاماملىماق 0x03000000ul
#define 사용자쪽수 ((ئىشلەتكۈچى_تاماملىماق - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ئىشلەتكۈچى_مەلۇمات_خاتالىق (-1001)
#define 사용자실행오류 (-1002)
#define ئىشلەتكۈچى_ئۈنۈمسىز_بۇيرۇق (-1003)
#define ئىشلەتكۈچى_ۋاقىت_ئاشتى (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t تىزىملىتىش_مەلۇمات[31], بۇيرۇق_ئورۇنلاشتۇرۇش, 상태값, دۆۋە_ئادرېس; } ئىشلەتكۈچى_رامكا;
void 사용자체계준비(void);
int 사용자예외(ئىشلەتكۈچى_رامكا *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t سۇپا_ئىشلەتكۈچى_قوزغىتىش(uintptr_t);
uintptr_t سۇپا_ئىشلەتكۈچى_دەلىللەش(void);
uintptr_t سۇپا_ئىشلەتكۈچى_تىزگىنى(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
