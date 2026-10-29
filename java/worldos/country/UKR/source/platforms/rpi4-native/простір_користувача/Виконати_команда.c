#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ПУСК_користувач_програма(int);
int користувач_ПУСК(int 전달값) {
    for (초기화함수 *дані_посада = __init_array_start; дані_посада < __init_array_end; дані_посада++) (*дані_посада)();
    int результат = ПУСК_користувач_програма(전달값);
    for (초기화함수 *дані_посада = __fini_array_end; дані_посада != __fini_array_start;) (*--дані_посада)();
    return результат;
}
void *memset(void *дані_посада, int значення, size_t 항목수) { unsigned char *місце_дані = дані_посада; while (항목수--) *місце_дані++ = значення; return дані_посада; }
void *memcpy(void *місце_дані, const void *рядок_дані, size_t 항목수) { unsigned char *첫째값 = місце_дані; const unsigned char *둘째값 = рядок_дані; while (항목수--) *첫째값++ = *둘째값++; return місце_дані; }
