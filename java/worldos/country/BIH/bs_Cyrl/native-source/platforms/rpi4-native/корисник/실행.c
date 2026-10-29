#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int почети_корисник_програм(int);
int корисник_почети(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = почети_корисник_програм(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int вриједност, size_t 항목수) { unsigned char *одредиште_подаци = 자료위치; while (항목수--) *одредиште_подаци++ = вриједност; return 자료위치; }
void *memcpy(void *одредиште_подаци, const void *стринг_подаци, size_t 항목수) { unsigned char *첫째값 = одредиште_подаци; const unsigned char *둘째값 = стринг_подаци; while (항목수--) *첫째값++ = *둘째값++; return одредиште_подаци; }
