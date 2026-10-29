#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int دەستپێك_بەکارهێنەر_بەرنامە(int);
int بەکارهێنەر_دەستپێك(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = دەستپێك_بەکارهێنەر_بەرنامە(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int نرخ, size_t 항목수) { unsigned char *جێمەبەست_دەیتا = 자료위치; while (항목수--) *جێمەبەست_دەیتا++ = نرخ; return 자료위치; }
void *memcpy(void *جێمەبەست_دەیتا, const void *رست_دەیتا, size_t 항목수) { unsigned char *첫째값 = جێمەبەست_دەیتا; const unsigned char *둘째값 = رست_دەیتا; while (항목수--) *첫째값++ = *둘째값++; return جێمەبەست_دەیتا; }
