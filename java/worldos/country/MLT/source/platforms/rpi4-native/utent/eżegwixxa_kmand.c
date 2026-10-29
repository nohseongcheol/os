#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Bidu_utent_programm(int);
int utent_Bidu(int 전달값) {
    for (초기화함수 *data_pożizzjoni = __init_array_start; data_pożizzjoni < __init_array_end; data_pożizzjoni++) (*data_pożizzjoni)();
    int miżura = Bidu_utent_programm(전달값);
    for (초기화함수 *data_pożizzjoni = __fini_array_end; data_pożizzjoni != __fini_array_start;) (*--data_pożizzjoni)();
    return miżura;
}
void *memset(void *data_pożizzjoni, int VALUE, size_t entrata_COUNT) { unsigned char *destinazzjoni_data = data_pożizzjoni; while (entrata_COUNT--) *destinazzjoni_data++ = VALUE; return data_pożizzjoni; }
void *memcpy(void *destinazzjoni_data, const void *string_data, size_t entrata_COUNT) { unsigned char *첫째값 = destinazzjoni_data; const unsigned char *SECOND_VALUE = string_data; while (entrata_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinazzjoni_data; }
