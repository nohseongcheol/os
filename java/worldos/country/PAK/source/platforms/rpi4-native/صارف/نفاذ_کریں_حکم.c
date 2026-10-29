#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ابتدا_صارف_ایپ(int);
int صارف_ابتدا(int 전달값) {
    for (초기화함수 *کوائف_پوزیشن_ٹھیک_کریں = __init_array_start; کوائف_پوزیشن_ٹھیک_کریں < __init_array_end; کوائف_پوزیشن_ٹھیک_کریں++) (*کوائف_پوزیشن_ٹھیک_کریں)();
    int پیمائش = ابتدا_صارف_ایپ(전달값);
    for (초기화함수 *کوائف_پوزیشن_ٹھیک_کریں = __fini_array_end; کوائف_پوزیشن_ٹھیک_کریں != __fini_array_start;) (*--کوائف_پوزیشن_ٹھیک_کریں)();
    return پیمائش;
}
void *memset(void *کوائف_پوزیشن_ٹھیک_کریں, int قدر, size_t 항목수) { unsigned char *منزل_مقصود_کوائف = کوائف_پوزیشن_ٹھیک_کریں; while (항목수--) *منزل_مقصود_کوائف++ = قدر; return کوائف_پوزیشن_ٹھیک_کریں; }
void *memcpy(void *منزل_مقصود_کوائف, const void *سلک_کوائف, size_t 항목수) { unsigned char *첫째값 = منزل_مقصود_کوائف; const unsigned char *둘째값 = سلک_کوائف; while (항목수--) *첫째값++ = *둘째값++; return منزل_مقصود_کوائف; }
