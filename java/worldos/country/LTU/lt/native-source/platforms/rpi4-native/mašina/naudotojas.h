#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define naudotojas_BASE 0x02000000ul
#define naudotojas_IMAGE_baigti_pokalbį 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define naudotojas_eilė_ADDRESS 0x02f00000ul
#define naudotojas_baigti_pokalbį 0x03000000ul
#define naudotojas_puslapis_COUNT ((naudotojas_baigti_pokalbį - naudotojas_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define 사용자자료오류 (-1001)
#define 사용자실행오류 (-1002)
#define 사용자잘못된명령 (-1003)
#define naudotojas_SKIRTASIS_LAIKAS (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registras_duomenys[31], komanda_padėtis, Būsena_CODE, eilė_ADDRESS; } naudotojas_kadras;
void 사용자체계준비(void);
int vartotojo_išimtinė_situacija(naudotojas_kadras *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Lenta_naudotojas_vykdyti(uintptr_t);
uintptr_t Lenta_naudotojas_tikrinti(void);
uintptr_t Lenta_vartotojo_valdiklis(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
