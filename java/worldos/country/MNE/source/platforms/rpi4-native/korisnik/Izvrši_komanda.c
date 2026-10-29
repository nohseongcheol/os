#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_korisnik_program(int);
int korisnik_START(int 전달값) {
    for (초기화함수 *podaci_pozicija = __init_array_start; podaci_pozicija < __init_array_end; podaci_pozicija++) (*podaci_pozicija)();
    int KR = START_korisnik_program(전달값);
    for (초기화함수 *podaci_pozicija = __fini_array_end; podaci_pozicija != __fini_array_start;) (*--podaci_pozicija)();
    return KR;
}
void *memset(void *podaci_pozicija, int VALUE, size_t stavka_COUNT_8f7753a1) { unsigned char *odredište_podaci = podaci_pozicija; while (stavka_COUNT_8f7753a1--) *odredište_podaci++ = VALUE; return podaci_pozicija; }
void *memcpy(void *odredište_podaci, const void *niska_podaci, size_t stavka_COUNT_8f7753a1) { unsigned char *첫째값 = odredište_podaci; const unsigned char *SECOND_VALUE = niska_podaci; while (stavka_COUNT_8f7753a1--) *첫째값++ = *SECOND_VALUE++; return odredište_podaci; }
