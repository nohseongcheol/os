#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int START_bruger_app(int);
int bruger_START(int 전달값) {
    for (초기화함수 *data_placere = __init_array_start; data_placere < __init_array_end; data_placere++) (*data_placere)();
    int KR = START_bruger_app(전달값);
    for (초기화함수 *data_placere = __fini_array_end; data_placere != __fini_array_start;) (*--data_placere)();
    return KR;
}
void *memset(void *data_placere, int VÆRDI, size_t post_TÆL_8f7753a1) { unsigned char *destination_data = data_placere; while (post_TÆL_8f7753a1--) *destination_data++ = VÆRDI; return data_placere; }
void *memcpy(void *destination_data, const void *streng_data, size_t post_TÆL_8f7753a1) { unsigned char *첫째값 = destination_data; const unsigned char *SEKUND_VÆRDI = streng_data; while (post_TÆL_8f7753a1--) *첫째값++ = *SEKUND_VÆRDI++; return destination_data; }
