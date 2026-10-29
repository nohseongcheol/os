#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int achuwalaa_ka_yataayakalü_akumajiaa(int);
int ka_yataayakalü_achuwalaa(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = achuwalaa_ka_yataayakalü_akumajiaa(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int ajutuu, size_t 항목수) { unsigned char *jalamüinjatü_atijaaya = 자료위치; while (항목수--) *jalamüinjatü_atijaaya++ = ajutuu; return 자료위치; }
void *memcpy(void *jalamüinjatü_atijaaya, const void *kaleena_atijaaya, size_t 항목수) { unsigned char *첫째값 = jalamüinjatü_atijaaya; const unsigned char *둘째값 = kaleena_atijaaya; while (항목수--) *첫째값++ = *둘째값++; return jalamüinjatü_atijaaya; }
