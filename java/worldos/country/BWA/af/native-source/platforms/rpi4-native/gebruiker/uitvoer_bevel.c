#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int BEGIN_gebruiker_program(int);
int gebruiker_BEGIN(int 전달값) {
    for (초기화함수 *data_plaas = __init_array_start; data_plaas < __init_array_end; data_plaas++) (*data_plaas)();
    int maatreël = BEGIN_gebruiker_program(전달값);
    for (초기화함수 *data_plaas = __fini_array_end; data_plaas != __fini_array_start;) (*--data_plaas)();
    return maatreël;
}
void *memset(void *data_plaas, int VALUE, size_t inskrywing_COUNT) { unsigned char *bestemming_data = data_plaas; while (inskrywing_COUNT--) *bestemming_data++ = VALUE; return data_plaas; }
void *memcpy(void *bestemming_data, const void *string_data, size_t inskrywing_COUNT) { unsigned char *첫째값 = bestemming_data; const unsigned char *SECOND_VALUE = string_data; while (inskrywing_COUNT--) *첫째값++ = *SECOND_VALUE++; return bestemming_data; }
