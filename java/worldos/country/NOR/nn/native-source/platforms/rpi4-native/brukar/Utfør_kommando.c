#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_brukar_app(int);
int brukar_START(int 전달값) {
    for (초기화함수 *data_plassere = __init_array_start; data_plassere < __init_array_end; data_plassere++) (*data_plassere)();
    int forretningsmål = START_brukar_app(전달값);
    for (초기화함수 *data_plassere = __fini_array_end; data_plassere != __fini_array_start;) (*--data_plassere)();
    return forretningsmål;
}
void *memset(void *data_plassere, int VALUE, size_t oppføring_COUNT) { unsigned char *mål_data = data_plassere; while (oppføring_COUNT--) *mål_data++ = VALUE; return data_plassere; }
void *memcpy(void *mål_data, const void *streng_data, size_t oppføring_COUNT) { unsigned char *첫째값 = mål_data; const unsigned char *SECOND_VALUE = streng_data; while (oppføring_COUNT--) *첫째값++ = *SECOND_VALUE++; return mål_data; }
