#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_používateľ_program(int);
int používateľ_START(int 전달값) {
    for (초기화함수 *údaje_pozícia = __init_array_start; údaje_pozícia < __init_array_end; údaje_pozícia++) (*údaje_pozícia)();
    int KR = START_používateľ_program(전달값);
    for (초기화함수 *údaje_pozícia = __fini_array_end; údaje_pozícia != __fini_array_start;) (*--údaje_pozícia)();
    return KR;
}
void *memset(void *údaje_pozícia, int VALUE, size_t položka_COUNT_8f7753a1) { unsigned char *cieľ_údaje = údaje_pozícia; while (položka_COUNT_8f7753a1--) *cieľ_údaje++ = VALUE; return údaje_pozícia; }
void *memcpy(void *cieľ_údaje, const void *reťazec_údaje, size_t položka_COUNT_8f7753a1) { unsigned char *첫째값 = cieľ_údaje; const unsigned char *SECOND_VALUE = reťazec_údaje; while (položka_COUNT_8f7753a1--) *첫째값++ = *SECOND_VALUE++; return cieľ_údaje; }
