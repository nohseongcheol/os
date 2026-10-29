#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_uporabnik_aplikacija(int);
int uporabnik_Start(int 전달값) {
    for (초기화함수 *podatki_položaj = __init_array_start; podatki_položaj < __init_array_end; podatki_položaj++) (*podatki_položaj)();
    int REZULTAT = Start_uporabnik_aplikacija(전달값);
    for (초기화함수 *podatki_položaj = __fini_array_end; podatki_položaj != __fini_array_start;) (*--podatki_položaj)();
    return REZULTAT;
}
void *memset(void *podatki_položaj, int VALUE, size_t vnos_COUNT) { unsigned char *cilj_podatki = podatki_položaj; while (vnos_COUNT--) *cilj_podatki++ = VALUE; return podatki_položaj; }
void *memcpy(void *cilj_podatki, const void *niz_podatki, size_t vnos_COUNT) { unsigned char *첫째값 = cilj_podatki; const unsigned char *SECOND_VALUE = niz_podatki; while (vnos_COUNT--) *첫째값++ = *SECOND_VALUE++; return cilj_podatki; }
