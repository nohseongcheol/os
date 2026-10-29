#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int nis_përdorues_program(int);
int përdorues_nis(int 전달값) {
    for (초기화함수 *të_dhëna_pozicioni = __init_array_start; të_dhëna_pozicioni < __init_array_end; të_dhëna_pozicioni++) (*të_dhëna_pozicioni)();
    int llogaritje = nis_përdorues_program(전달값);
    for (초기화함수 *të_dhëna_pozicioni = __fini_array_end; të_dhëna_pozicioni != __fini_array_start;) (*--të_dhëna_pozicioni)();
    return llogaritje;
}
void *memset(void *të_dhëna_pozicioni, int VALUE, size_t futje_COUNT) { unsigned char *vendmbërritje_të_dhëna = të_dhëna_pozicioni; while (futje_COUNT--) *vendmbërritje_të_dhëna++ = VALUE; return të_dhëna_pozicioni; }
void *memcpy(void *vendmbërritje_të_dhëna, const void *varg_të_dhëna, size_t futje_COUNT) { unsigned char *첫째값 = vendmbërritje_të_dhëna; const unsigned char *SECOND_VALUE = varg_të_dhëna; while (futje_COUNT--) *첫째값++ = *SECOND_VALUE++; return vendmbërritje_të_dhëna; }
