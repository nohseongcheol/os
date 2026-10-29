#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define ଉପଭୋକ୍ତା_ଚିତ୍ର_ଶେଷ_କରନ୍ତୁ 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define ଉପଭୋକ୍ତା_ଗଦା_ଠିକଣା 0x02f00000ul
#define ଉପଭୋକ୍ତା_ଶେଷ_କରନ୍ତୁ 0x03000000ul
#define 사용자쪽수 ((ଉପଭୋକ୍ତା_ଶେଷ_କରନ୍ତୁ - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define ଉପଭୋକ୍ତା_ଡାଟା_ତ୍ରୁଟି (-1001)
#define 사용자실행오류 (-1002)
#define ଉପଭୋକ୍ତା_ଅବୈଧ_ପରାମର୍ଶ (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ଡାଟା[31], ନିର୍ଦ୍ଦେଶ_ସ୍ଥିତି, 상태값, ଗଦା_ଠିକଣା; } ଉପଭୋକ୍ତା_ଫ୍ରେମ୍;
void 사용자체계준비(void);
int ଉପଭୋକ୍ତା_ବ୍ୟତିକ୍ରମ(ଉପଭୋକ୍ତା_ଫ୍ରେମ୍ *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t ବୋର୍ଡ୍_ଉପଭୋକ୍ତା_ରନ୍(uintptr_t);
uintptr_t ବୋର୍ଡ୍_ଉପଭୋକ୍ତା_ବୈଧକରଣ(void);
uintptr_t ବୋର୍ଡ୍_ଉପଭୋକ୍ତା_ନିୟନ୍ତ୍ରଣ(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
