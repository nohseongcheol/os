#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Баштоо_колдонуучу_програм(int);
int колдонуучу_Баштоо(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Баштоо_колдонуучу_програм(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int маани, size_t 항목수) { unsigned char *көздөө_жайы_берилмелер = 자료위치; while (항목수--) *көздөө_жайы_берилмелер++ = маани; return 자료위치; }
void *memcpy(void *көздөө_жайы_берилмелер, const void *сап_берилмелер, size_t 항목수) { unsigned char *첫째값 = көздөө_жайы_берилмелер; const unsigned char *둘째값 = сап_берилмелер; while (항목수--) *첫째값++ = *둘째값++; return көздөө_жайы_берилмелер; }
