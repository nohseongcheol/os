#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_användare_app(int);
int användare_START(int 전달값) {
    for (초기화함수 *data_placera = __init_array_start; data_placera < __init_array_end; data_placera++) (*data_placera)();
    int RESULTAT = START_användare_app(전달값);
    for (초기화함수 *data_placera = __fini_array_end; data_placera != __fini_array_start;) (*--data_placera)();
    return RESULTAT;
}
void *memset(void *data_placera, int värde, size_t post_ANTAL) { unsigned char *mål_data = data_placera; while (post_ANTAL--) *mål_data++ = värde; return data_placera; }
void *memcpy(void *mål_data, const void *sträng_data, size_t post_ANTAL) { unsigned char *첫째값 = mål_data; const unsigned char *SEKUND_värde = sträng_data; while (post_ANTAL--) *첫째값++ = *SEKUND_värde++; return mål_data; }
