#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int 사용자시작(int);
int 사용자진입연결(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int ИСХОД = 사용자시작(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return ИСХОД;
}
void *memset(void *자료위치, int 값, size_t 항목수) { unsigned char *목적자료 = 자료위치; while (항목수--) *목적자료++ = 값; return 자료위치; }
void *memcpy(void *목적자료, const void *문자열값, size_t 항목수) { unsigned char *첫째값 = 목적자료; const unsigned char *둘째값 = 문자열값; while (항목수--) *첫째값++ = *둘째값++; return 목적자료; }
