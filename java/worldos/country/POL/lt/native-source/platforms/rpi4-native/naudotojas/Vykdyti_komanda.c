#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_naudotojas_programa(int);
int naudotojas_Start(int 전달값) {
    for (초기화함수 *duomenys_padėtis = __init_array_start; duomenys_padėtis < __init_array_end; duomenys_padėtis++) (*duomenys_padėtis)();
    int REZULTATAS = Start_naudotojas_programa(전달값);
    for (초기화함수 *duomenys_padėtis = __fini_array_end; duomenys_padėtis != __fini_array_start;) (*--duomenys_padėtis)();
    return REZULTATAS;
}
void *memset(void *duomenys_padėtis, int VALUE, size_t įrašas_COUNT) { unsigned char *vieta_duomenys = duomenys_padėtis; while (įrašas_COUNT--) *vieta_duomenys++ = VALUE; return duomenys_padėtis; }
void *memcpy(void *vieta_duomenys, const void *eilutė_duomenys, size_t įrašas_COUNT) { unsigned char *첫째값 = vieta_duomenys; const unsigned char *SECOND_VALUE = eilutė_duomenys; while (įrašas_COUNT--) *첫째값++ = *SECOND_VALUE++; return vieta_duomenys; }
