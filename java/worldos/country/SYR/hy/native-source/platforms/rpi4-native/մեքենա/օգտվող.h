#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define օգտվող_նկար_վերջացնել 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define օգտվող_Շեղջ_հասցե 0x02f00000ul
#define օգտվող_վերջացնել 0x03000000ul
#define 사용자쪽수 ((օգտվող_վերջացնել - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define օգտվող_տվյալ_սխալ (-1001)
#define 사용자실행오류 (-1002)
#define օգտվող_անվավեր_հրահանգ (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t գրանցվել_տվյալ[31], հրաման_դիրք, վիճակ_կոդ, Շեղջ_հասցե; } օգտվող_կադր;
void 사용자체계준비(void);
int 사용자예외(օգտվող_կադր *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t տախտակ_օգտվող_աշխատեցնել(uintptr_t);
uintptr_t տախտակ_օգտվող_վավերացնել(void);
uintptr_t տախտակ_օգտվողի_կառավար(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
