#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int qala_umsebenzisi_inkqubo(int);
int umsebenzisi_qala(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = qala_umsebenzisi_inkqubo(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int ixabiso, size_t 항목수) { unsigned char *indawo_ekuyiwa_kuyo_iingcombolo = 자료위치; while (항목수--) *indawo_ekuyiwa_kuyo_iingcombolo++ = ixabiso; return 자료위치; }
void *memcpy(void *indawo_ekuyiwa_kuyo_iingcombolo, const void *uluhlu_lweekharektha_iingcombolo, size_t 항목수) { unsigned char *첫째값 = indawo_ekuyiwa_kuyo_iingcombolo; const unsigned char *둘째값 = uluhlu_lweekharektha_iingcombolo; while (항목수--) *첫째값++ = *둘째값++; return indawo_ekuyiwa_kuyo_iingcombolo; }
