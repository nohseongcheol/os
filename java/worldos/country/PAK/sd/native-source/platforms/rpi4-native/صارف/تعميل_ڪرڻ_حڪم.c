#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int شروع_صارف_ائپ(int);
int صارف_شروع(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = شروع_صارف_ائپ(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int قدر, size_t 항목수) { unsigned char *منزل_مقصود_ڪوائف = 자료위치; while (항목수--) *منزل_مقصود_ڪوائف++ = قدر; return 자료위치; }
void *memcpy(void *منزل_مقصود_ڪوائف, const void *اسٽرنگ_ڪوائف, size_t 항목수) { unsigned char *첫째값 = منزل_مقصود_ڪوائف; const unsigned char *둘째값 = اسٽرنگ_ڪوائف; while (항목수--) *첫째값++ = *둘째값++; return منزل_مقصود_ڪوائف; }
