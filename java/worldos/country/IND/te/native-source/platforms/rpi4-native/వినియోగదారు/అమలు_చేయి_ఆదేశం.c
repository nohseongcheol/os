#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ప్రారంభం_వినియోగదారు_అనువర్తనం(int);
int వినియోగదారు_ప్రారంభం(int 전달값) {
    for (초기화함수 *డేటా_స్థాయి = __init_array_start; డేటా_స్థాయి < __init_array_end; డేటా_స్థాయి++) (*డేటా_స్థాయి)();
    int ప్రమాణం = ప్రారంభం_వినియోగదారు_అనువర్తనం(전달값);
    for (초기화함수 *డేటా_స్థాయి = __fini_array_end; డేటా_స్థాయి != __fini_array_start;) (*--డేటా_స్థాయి)();
    return ప్రమాణం;
}
void *memset(void *డేటా_స్థాయి, int మూల్యం, size_t 항목수) { unsigned char *గమ్యం_డేటా = డేటా_స్థాయి; while (항목수--) *గమ్యం_డేటా++ = మూల్యం; return డేటా_స్థాయి; }
void *memcpy(void *గమ్యం_డేటా, const void *అక్షరసరం_డేటా, size_t 항목수) { unsigned char *첫째값 = గమ్యం_డేటా; const unsigned char *둘째값 = అక్షరసరం_డేటా; while (항목수--) *첫째값++ = *둘째값++; return గమ్యం_డేటా; }
