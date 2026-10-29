#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_gebruiker_app(int);
int gebruiker_START(int 전달값) {
    for (초기화함수 *gegevens_functie = __init_array_start; gegevens_functie < __init_array_end; gegevens_functie++) (*gegevens_functie)();
    int resultaat = START_gebruiker_app(전달값);
    for (초기화함수 *gegevens_functie = __fini_array_end; gegevens_functie != __fini_array_start;) (*--gegevens_functie)();
    return resultaat;
}
void *memset(void *gegevens_functie, int WAARDE, size_t invoer_AANTAL_8f7753a1) { unsigned char *doel_gegevens = gegevens_functie; while (invoer_AANTAL_8f7753a1--) *doel_gegevens++ = WAARDE; return gegevens_functie; }
void *memcpy(void *doel_gegevens, const void *tekenreeks_gegevens, size_t invoer_AANTAL_8f7753a1) { unsigned char *첫째값 = doel_gegevens; const unsigned char *SECONDE_WAARDE = tekenreeks_gegevens; while (invoer_AANTAL_8f7753a1--) *첫째값++ = *SECONDE_WAARDE++; return doel_gegevens; }
