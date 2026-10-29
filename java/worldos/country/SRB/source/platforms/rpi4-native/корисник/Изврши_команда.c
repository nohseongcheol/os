#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Старт_корисник_програм(int);
int корисник_Старт(int 전달값) {
    for (초기화함수 *подаци_позиција = __init_array_start; подаци_позиција < __init_array_end; подаци_позиција++) (*подаци_позиција)();
    int ИСХОД = Старт_корисник_програм(전달값);
    for (초기화함수 *подаци_позиција = __fini_array_end; подаци_позиција != __fini_array_start;) (*--подаци_позиција)();
    return ИСХОД;
}
void *memset(void *подаци_позиција, int вриједност, size_t 항목수) { unsigned char *одредиште_подаци = подаци_позиција; while (항목수--) *одредиште_подаци++ = вриједност; return подаци_позиција; }
void *memcpy(void *одредиште_подаци, const void *ниска_подаци, size_t 항목수) { unsigned char *첫째값 = одредиште_подаци; const unsigned char *둘째값 = ниска_подаци; while (항목수--) *첫째값++ = *둘째값++; return одредиште_подаци; }
