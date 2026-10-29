#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define صارف_نقش_ختم_ڪريو 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define صارف_اڀرڻ_پتو 0x02f00000ul
#define صارف_ختم_ڪريو 0x03000000ul
#define 사용자쪽수 ((صارف_ختم_ڪريو - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define صارف_ڪوائف_نقص (-1001)
#define 사용자실행오류 (-1002)
#define صارف_ناجائز_هدايت (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t 저장기값[31], 명령위치, 상태값, اڀرڻ_پتو; } صارف_فريم;
void 사용자체계준비(void);
int 사용자예외(صارف_فريم *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t 보드사용자실행(uintptr_t);
uintptr_t 보드사용자검사(void);
uintptr_t 보드사용자제어(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
