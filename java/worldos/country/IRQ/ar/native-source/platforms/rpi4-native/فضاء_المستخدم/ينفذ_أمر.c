#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int بدء_مستخدم_تطبيق(int);
int مستخدم_بدء(int 전달값) {
    for (초기화함수 *بيانات_منصب = __init_array_start; بيانات_منصب < __init_array_end; بيانات_منصب++) (*بيانات_منصب)();
    int نتيجة = بدء_مستخدم_تطبيق(전달값);
    for (초기화함수 *بيانات_منصب = __fini_array_end; بيانات_منصب != __fini_array_start;) (*--بيانات_منصب)();
    return نتيجة;
}
void *memset(void *بيانات_منصب, int قيمة, size_t 항목수) { unsigned char *وجهة_بيانات = بيانات_منصب; while (항목수--) *وجهة_بيانات++ = قيمة; return بيانات_منصب; }
void *memcpy(void *وجهة_بيانات, const void *سلسلة_بيانات, size_t 항목수) { unsigned char *첫째값 = وجهة_بيانات; const unsigned char *둘째값 = سلسلة_بيانات; while (항목수--) *첫째값++ = *둘째값++; return وجهة_بيانات; }
