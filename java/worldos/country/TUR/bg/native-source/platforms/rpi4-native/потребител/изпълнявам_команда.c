#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Старт_потребител_програма(int);
int потребител_Старт(int 전달값) {
    for (초기화함수 *данни_позиция = __init_array_start; данни_позиция < __init_array_end; данни_позиция++) (*данни_позиция)();
    int РЕЗУЛТАТ = Старт_потребител_програма(전달값);
    for (초기화함수 *данни_позиция = __fini_array_end; данни_позиция != __fini_array_start;) (*--данни_позиция)();
    return РЕЗУЛТАТ;
}
void *memset(void *данни_позиция, int стойност, size_t 항목수) { unsigned char *местоназначение_данни = данни_позиция; while (항목수--) *местоназначение_данни++ = стойност; return данни_позиция; }
void *memcpy(void *местоназначение_данни, const void *низ_данни, size_t 항목수) { unsigned char *첫째값 = местоназначение_данни; const unsigned char *둘째값 = низ_данни; while (항목수--) *첫째값++ = *둘째값++; return местоназначение_данни; }
