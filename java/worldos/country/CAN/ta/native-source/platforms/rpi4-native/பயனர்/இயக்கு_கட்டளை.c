#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int தொடங்கு_பயனர்_நிரல்(int);
int பயனர்_தொடங்கு(int 전달값) {
    for (초기화함수 *தரவு_நிலை = __init_array_start; தரவு_நிலை < __init_array_end; தரவு_நிலை++) (*தரவு_நிலை)();
    int அளவிடக்கூடியது = தொடங்கு_பயனர்_நிரல்(전달값);
    for (초기화함수 *தரவு_நிலை = __fini_array_end; தரவு_நிலை != __fini_array_start;) (*--தரவு_நிலை)();
    return அளவிடக்கூடியது;
}
void *memset(void *தரவு_நிலை, int மதிப்பு, size_t 항목수) { unsigned char *இலக்கு_தரவு = தரவு_நிலை; while (항목수--) *இலக்கு_தரவு++ = மதிப்பு; return தரவு_நிலை; }
void *memcpy(void *இலக்கு_தரவு, const void *சரம்_தரவு, size_t 항목수) { unsigned char *첫째값 = இலக்கு_தரவு; const unsigned char *둘째값 = சரம்_தரவு; while (항목수--) *첫째값++ = *둘째값++; return இலக்கு_தரவு; }
