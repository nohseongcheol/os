#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_bruker_app(int);
int bruker_START(int 전달값) {
    for (초기화함수 *data_plassere = __init_array_start; data_plassere < __init_array_end; data_plassere++) (*data_plassere)();
    int KR = START_bruker_app(전달값);
    for (초기화함수 *data_plassere = __fini_array_end; data_plassere != __fini_array_start;) (*--data_plassere)();
    return KR;
}
void *memset(void *data_plassere, int VERDI, size_t oppføring_ANTALL) { unsigned char *mål_data = data_plassere; while (oppføring_ANTALL--) *mål_data++ = VERDI; return data_plassere; }
void *memcpy(void *mål_data, const void *streng_data, size_t oppføring_ANTALL) { unsigned char *첫째값 = mål_data; const unsigned char *SEKUND_VERDI = streng_data; while (oppføring_ANTALL--) *첫째값++ = *SEKUND_VERDI++; return mål_data; }
