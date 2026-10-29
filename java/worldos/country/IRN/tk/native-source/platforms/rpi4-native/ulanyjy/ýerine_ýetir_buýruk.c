#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int başlat_ulanyjy_programma(int);
int ulanyjy_başlat(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = başlat_ulanyjy_programma(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int baha, size_t 항목수) { unsigned char *barylmaly_ýer_maglumat = 자료위치; while (항목수--) *barylmaly_ýer_maglumat++ = baha; return 자료위치; }
void *memcpy(void *barylmaly_ýer_maglumat, const void *setir_maglumat, size_t 항목수) { unsigned char *첫째값 = barylmaly_ýer_maglumat; const unsigned char *둘째값 = setir_maglumat; while (항목수--) *첫째값++ = *둘째값++; return barylmaly_ýer_maglumat; }
