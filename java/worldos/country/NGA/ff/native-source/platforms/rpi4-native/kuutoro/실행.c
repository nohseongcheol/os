#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int huɓɓude_kuutoro_tafirde(int);
int kuutoro_huɓɓude(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = huɓɓude_kuutoro_tafirde(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int njaru, size_t 항목수) { unsigned char *tiindaare_keɓe = 자료위치; while (항목수--) *tiindaare_keɓe++ = njaru; return 자료위치; }
void *memcpy(void *tiindaare_keɓe, const void *ɓoggol_keɓe, size_t 항목수) { unsigned char *첫째값 = tiindaare_keɓe; const unsigned char *둘째값 = ɓoggol_keɓe; while (항목수--) *첫째값++ = *둘째값++; return tiindaare_keɓe; }
