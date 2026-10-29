#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int buta_utilizator_program(int);
int utilizator_buta(int 전달값) {
    for (초기화함수 *date_poziție = __init_array_start; date_poziție < __init_array_end; date_poziție++) (*date_poziție)();
    int KR = buta_utilizator_program(전달값);
    for (초기화함수 *date_poziție = __fini_array_end; date_poziție != __fini_array_start;) (*--date_poziție)();
    return KR;
}
void *memset(void *date_poziție, int VALUE, size_t intrare_COUNT) { unsigned char *destinație_date = date_poziție; while (intrare_COUNT--) *destinație_date++ = VALUE; return date_poziție; }
void *memcpy(void *destinație_date, const void *șir_date, size_t intrare_COUNT) { unsigned char *첫째값 = destinație_date; const unsigned char *SECOND_VALUE = șir_date; while (intrare_COUNT--) *첫째값++ = *SECOND_VALUE++; return destinație_date; }
