#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_корисник_програма(int);
int корисник_Start(int 전달값) {
    for (초기화함수 *податоци_позиционирање = __init_array_start; податоци_позиционирање < __init_array_end; податоци_позиционирање++) (*податоци_позиционирање)();
    int мерка = Start_корисник_програма(전달값);
    for (초기화함수 *податоци_позиционирање = __fini_array_end; податоци_позиционирање != __fini_array_start;) (*--податоци_позиционирање)();
    return мерка;
}
void *memset(void *податоци_позиционирање, int VALUE, size_t внес_COUNT) { unsigned char *одредиште_податоци = податоци_позиционирање; while (внес_COUNT--) *одредиште_податоци++ = VALUE; return податоци_позиционирање; }
void *memcpy(void *одредиште_податоци, const void *низа_податоци, size_t внес_COUNT) { unsigned char *첫째값 = одредиште_податоци; const unsigned char *SECOND_VALUE = низа_податоци; while (внес_COUNT--) *첫째값++ = *SECOND_VALUE++; return одредиште_податоци; }
