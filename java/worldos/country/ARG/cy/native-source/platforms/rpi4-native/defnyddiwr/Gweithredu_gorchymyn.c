#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_defnyddiwr_Rhaglen(int);
int defnyddiwr_START(int 전달값) {
    for (초기화함수 *data_safle = __init_array_start; data_safle < __init_array_end; data_safle++) (*data_safle)();
    int mesur = START_defnyddiwr_Rhaglen(전달값);
    for (초기화함수 *data_safle = __fini_array_end; data_safle != __fini_array_start;) (*--data_safle)();
    return mesur;
}
void *memset(void *data_safle, int VALUE, size_t cofnod_COUNT) { unsigned char *cyrchfan_data = data_safle; while (cofnod_COUNT--) *cyrchfan_data++ = VALUE; return data_safle; }
void *memcpy(void *cyrchfan_data, const void *testun_data, size_t cofnod_COUNT) { unsigned char *첫째값 = cyrchfan_data; const unsigned char *SECOND_VALUE = testun_data; while (cofnod_COUNT--) *첫째값++ = *SECOND_VALUE++; return cyrchfan_data; }
