#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_kasutaja_programm(int);
int kasutaja_START(int 전달값) {
    for (초기화함수 *andmed_ametikoht = __init_array_start; andmed_ametikoht < __init_array_end; andmed_ametikoht++) (*andmed_ametikoht)();
    int TULEMUS = START_kasutaja_programm(전달값);
    for (초기화함수 *andmed_ametikoht = __fini_array_end; andmed_ametikoht != __fini_array_start;) (*--andmed_ametikoht)();
    return TULEMUS;
}
void *memset(void *andmed_ametikoht, int VALUE, size_t kirje_COUNT) { unsigned char *sihtkoht_andmed = andmed_ametikoht; while (kirje_COUNT--) *sihtkoht_andmed++ = VALUE; return andmed_ametikoht; }
void *memcpy(void *sihtkoht_andmed, const void *string_andmed, size_t kirje_COUNT) { unsigned char *첫째값 = sihtkoht_andmed; const unsigned char *SECOND_VALUE = string_andmed; while (kirje_COUNT--) *첫째값++ = *SECOND_VALUE++; return sihtkoht_andmed; }
