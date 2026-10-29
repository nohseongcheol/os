#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Эхлэл_хэрэглэгч_програм(int);
int хэрэглэгч_Эхлэл(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Эхлэл_хэрэглэгч_програм(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int утга, size_t 항목수) { unsigned char *товлосон_газар_өгөгдөл = 자료위치; while (항목수--) *товлосон_газар_өгөгдөл++ = утга; return 자료위치; }
void *memcpy(void *товлосон_газар_өгөгдөл, const void *мөр_өгөгдөл, size_t 항목수) { unsigned char *첫째값 = товлосон_газар_өгөгдөл; const unsigned char *둘째값 = мөр_өгөгдөл; while (항목수--) *첫째값++ = *둘째값++; return товлосон_газар_өгөгдөл; }
