#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_korisnik_program(int);
int korisnik_START(int 전달값) {
    for (초기화함수 *podaci_položaj = __init_array_start; podaci_položaj < __init_array_end; podaci_položaj++) (*podaci_položaj)();
    int mjera = START_korisnik_program(전달값);
    for (초기화함수 *podaci_položaj = __fini_array_end; podaci_položaj != __fini_array_start;) (*--podaci_položaj)();
    return mjera;
}
void *memset(void *podaci_položaj, int VALUE, size_t unos_COUNT) { unsigned char *odredište_podaci = podaci_položaj; while (unos_COUNT--) *odredište_podaci++ = VALUE; return podaci_položaj; }
void *memcpy(void *odredište_podaci, const void *string_podaci, size_t unos_COUNT) { unsigned char *첫째값 = odredište_podaci; const unsigned char *SECOND_VALUE = string_podaci; while (unos_COUNT--) *첫째값++ = *SECOND_VALUE++; return odredište_podaci; }
