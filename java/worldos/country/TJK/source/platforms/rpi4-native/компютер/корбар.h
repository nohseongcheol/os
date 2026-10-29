#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define корбар_расм_анҷом_додан 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define корбар_ҷамъ_суроға 0x02f00000ul
#define корбар_анҷом_додан 0x03000000ul
#define 사용자쪽수 ((корбар_анҷом_додан - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define корбар_иттилоот_хато (-1001)
#define 사용자실행오류 (-1002)
#define корбар_беэътибор_дастур (-1003)
#define 사용자시간초과 (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t қайд_кардан_иттилоот[31], 명령위치, 상태값, ҷамъ_суроға; } корбар_чорчӯба;
void 사용자체계준비(void);
int 사용자예외(корбар_чорчӯба *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t 보드사용자실행(uintptr_t);
uintptr_t 보드사용자검사(void);
uintptr_t 보드사용자제어(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
