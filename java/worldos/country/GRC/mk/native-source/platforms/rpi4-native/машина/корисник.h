#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define корисник_BASE 0x02000000ul
#define корисник_IMAGE_крај 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define корисник_Купче_адреса 0x02f00000ul
#define корисник_крај 0x03000000ul
#define корисник_страница_COUNT ((корисник_крај - корисник_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define корисник_податоци_грешка (-1001)
#define 사용자실행오류 (-1002)
#define корисник_неважечки_инструкција (-1003)
#define корисник_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t регистрирај_податоци[31], наредба_позиционирање, статус_CODE, Купче_адреса; } корисник_врами;
void 사용자체계준비(void);
int корисник_исклучок(корисник_врами *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t табла_корисник_изврши(uintptr_t);
uintptr_t табла_корисник_потврди(void);
uintptr_t табла_корисничка_контрола(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
