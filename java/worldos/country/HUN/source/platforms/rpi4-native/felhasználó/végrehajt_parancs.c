#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_felhasználó_app(int);
int felhasználó_START(int 전달값) {
    for (초기화함수 *adat_pozíció = __init_array_start; adat_pozíció < __init_array_end; adat_pozíció++) (*adat_pozíció)();
    int KR = START_felhasználó_app(전달값);
    for (초기화함수 *adat_pozíció = __fini_array_end; adat_pozíció != __fini_array_start;) (*--adat_pozíció)();
    return KR;
}
void *memset(void *adat_pozíció, int ÉRTÉK, size_t bejegyzés_DARAB) { unsigned char *cél_adat = adat_pozíció; while (bejegyzés_DARAB--) *cél_adat++ = ÉRTÉK; return adat_pozíció; }
void *memcpy(void *cél_adat, const void *sztring_adat, size_t bejegyzés_DARAB) { unsigned char *첫째값 = cél_adat; const unsigned char *MPERC_ÉRTÉK = sztring_adat; while (bejegyzés_DARAB--) *첫째값++ = *MPERC_ÉRTÉK++; return cél_adat; }
