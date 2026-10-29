#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Оғоз_корбар_барнома(int);
int корбар_Оғоз(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Оғоз_корбар_барнома(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int қимат, size_t 항목수) { unsigned char *ҷои_таъинот_иттилоот = 자료위치; while (항목수--) *ҷои_таъинот_иттилоот++ = қимат; return 자료위치; }
void *memcpy(void *ҷои_таъинот_иттилоот, const void *сатр_иттилоот, size_t 항목수) { unsigned char *첫째값 = ҷои_таъинот_иттилоот; const unsigned char *둘째값 = сатр_иттилоот; while (항목수--) *첫째값++ = *둘째값++; return ҷои_таъинот_иттилоот; }
