#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Пуск_карыстальнік_праграма(int);
int карыстальнік_Пуск(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Пуск_карыстальнік_праграма(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int значэнне, size_t 항목수) { unsigned char *прызначэнне_дадзеныя = 자료위치; while (항목수--) *прызначэнне_дадзеныя++ = значэнне; return 자료위치; }
void *memcpy(void *прызначэнне_дадзеныя, const void *радок_дадзеныя, size_t 항목수) { unsigned char *첫째값 = прызначэнне_дадзеныя; const unsigned char *둘째값 = радок_дадзеныя; while (항목수--) *첫째값++ = *둘째값++; return прызначэнне_дадзеныя; }
