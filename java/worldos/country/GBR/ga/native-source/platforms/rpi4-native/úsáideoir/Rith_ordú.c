#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_úsáideoir_clár(int);
int úsáideoir_Start(int 전달값) {
    for (초기화함수 *sonraí_suíomh = __init_array_start; sonraí_suíomh < __init_array_end; sonraí_suíomh++) (*sonraí_suíomh)();
    int tomhas = Start_úsáideoir_clár(전달값);
    for (초기화함수 *sonraí_suíomh = __fini_array_end; sonraí_suíomh != __fini_array_start;) (*--sonraí_suíomh)();
    return tomhas;
}
void *memset(void *sonraí_suíomh, int VALUE, size_t iontráil_COUNT) { unsigned char *sprioc_sonraí = sonraí_suíomh; while (iontráil_COUNT--) *sprioc_sonraí++ = VALUE; return sonraí_suíomh; }
void *memcpy(void *sprioc_sonraí, const void *teaghrán_sonraí, size_t iontráil_COUNT) { unsigned char *첫째값 = sprioc_sonraí; const unsigned char *SECOND_VALUE = teaghrán_sonraí; while (iontráil_COUNT--) *첫째값++ = *SECOND_VALUE++; return sprioc_sonraí; }
