#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define 사용자바탕 0x02000000ul
#define пайдаланушы_сурет_тоқтату 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define пайдаланушы_Бума_мекенжай 0x02f00000ul
#define пайдаланушы_тоқтату 0x03000000ul
#define 사용자쪽수 ((пайдаланушы_тоқтату - 사용자바탕) / 4096ul)
#define 사용자실행파일오류 (-8)
#define пайдаланушы_деректер_қате (-1001)
#define 사용자실행오류 (-1002)
#define пайдаланушы_дұрыс_емес_нұсқау (-1003)
#define пайдаланушы_ТАЙМ_АУТ (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t тіркеу_деректер[31], пәрмен_лауазым, күй_код, Бума_мекенжай; } пайдаланушы_кадр;
void 사용자체계준비(void);
int пайдаланушы_ерекшелік(пайдаланушы_кадр *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Тақта_пайдаланушы_орындалу(uintptr_t);
uintptr_t Тақта_пайдаланушы_тексеру(void);
uintptr_t Тақта_пайдаланушының_басқару_элементі(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
