#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_gumagamit_app(int);
int gumagamit_Start(int 전달값) {
    for (초기화함수 *data_posisyon = __init_array_start; data_posisyon < __init_array_end; data_posisyon++) (*data_posisyon)();
    int sukat = Start_gumagamit_app(전달값);
    for (초기화함수 *data_posisyon = __fini_array_end; data_posisyon != __fini_array_start;) (*--data_posisyon)();
    return sukat;
}
void *memset(void *data_posisyon, int VALUE, size_t pagpasok_COUNT) { unsigned char *patutunguhan_data = data_posisyon; while (pagpasok_COUNT--) *patutunguhan_data++ = VALUE; return data_posisyon; }
void *memcpy(void *patutunguhan_data, const void *string_data, size_t pagpasok_COUNT) { unsigned char *첫째값 = patutunguhan_data; const unsigned char *SECOND_VALUE = string_data; while (pagpasok_COUNT--) *첫째값++ = *SECOND_VALUE++; return patutunguhan_data; }
