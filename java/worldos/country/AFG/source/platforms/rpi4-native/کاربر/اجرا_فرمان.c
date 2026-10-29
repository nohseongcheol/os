#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int شروع_کاربر_برنامه(int);
int کاربر_شروع(int 전달값) {
    for (초기화함수 *داده_ها_مرتب_کردن = __init_array_start; داده_ها_مرتب_کردن < __init_array_end; داده_ها_مرتب_کردن++) (*داده_ها_مرتب_کردن)();
    int سنجش = شروع_کاربر_برنامه(전달값);
    for (초기화함수 *داده_ها_مرتب_کردن = __fini_array_end; داده_ها_مرتب_کردن != __fini_array_start;) (*--داده_ها_مرتب_کردن)();
    return سنجش;
}
void *memset(void *داده_ها_مرتب_کردن, int مقدار, size_t 항목수) { unsigned char *مقصد_داده_ها = داده_ها_مرتب_کردن; while (항목수--) *مقصد_داده_ها++ = مقدار; return داده_ها_مرتب_کردن; }
void *memcpy(void *مقصد_داده_ها, const void *رشته_داده_ها, size_t 항목수) { unsigned char *첫째값 = مقصد_داده_ها; const unsigned char *둘째값 = رشته_داده_ها; while (항목수--) *첫째값++ = *둘째값++; return مقصد_داده_ها; }
