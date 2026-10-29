#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int پيل_کارن_کاريال(int);
int کارن_پيل(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = پيل_کارن_کاريال(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int ارزښت, size_t 항목수) { unsigned char *موخه_اومتوک = 자료위치; while (항목수--) *موخه_اومتوک++ = ارزښت; return 자료위치; }
void *memcpy(void *موخه_اومتوک, const void *مزى_اومتوک, size_t 항목수) { unsigned char *첫째값 = موخه_اومتوک; const unsigned char *둘째값 = مزى_اومتوک; while (항목수--) *첫째값++ = *둘째값++; return موخه_اومتوک; }
