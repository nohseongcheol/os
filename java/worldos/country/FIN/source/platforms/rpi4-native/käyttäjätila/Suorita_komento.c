#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int alku_käyttäjä_ohjelma(int);
int käyttäjä_alku(int 전달값) {
    for (초기화함수 *data_toimi = __init_array_start; data_toimi < __init_array_end; data_toimi++) (*data_toimi)();
    int TULOS = alku_käyttäjä_ohjelma(전달값);
    for (초기화함수 *data_toimi = __fini_array_end; data_toimi != __fini_array_start;) (*--data_toimi)();
    return TULOS;
}
void *memset(void *data_toimi, int ARVO, size_t merkintä_LASKE) { unsigned char *kohde_data = data_toimi; while (merkintä_LASKE--) *kohde_data++ = ARVO; return data_toimi; }
void *memcpy(void *kohde_data, const void *merkkijono_data, size_t merkintä_LASKE) { unsigned char *첫째값 = kohde_data; const unsigned char *SEKUNNIT_ARVO = merkkijono_data; while (merkintä_LASKE--) *첫째값++ = *SEKUNNIT_ARVO++; return kohde_data; }
