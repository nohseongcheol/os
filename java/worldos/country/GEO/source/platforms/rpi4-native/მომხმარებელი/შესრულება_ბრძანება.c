#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int დაწყება_მომხმარებელი_აპი(int);
int მომხმარებელი_დაწყება(int 전달값) {
    for (초기화함수 *მონაცემები_პოზიცია = __init_array_start; მონაცემები_პოზიცია < __init_array_end; მონაცემები_პოზიცია++) (*მონაცემები_პოზიცია)();
    int გაზომვა = დაწყება_მომხმარებელი_აპი(전달값);
    for (초기화함수 *მონაცემები_პოზიცია = __fini_array_end; მონაცემები_პოზიცია != __fini_array_start;) (*--მონაცემები_პოზიცია)();
    return გაზომვა;
}
void *memset(void *მონაცემები_პოზიცია, int მნიშვნელობა, size_t 항목수) { unsigned char *მიმართულება_მონაცემები = მონაცემები_პოზიცია; while (항목수--) *მიმართულება_მონაცემები++ = მნიშვნელობა; return მონაცემები_პოზიცია; }
void *memcpy(void *მიმართულება_მონაცემები, const void *სტრიქონი_მონაცემები, size_t 항목수) { unsigned char *첫째값 = მიმართულება_მონაცემები; const unsigned char *둘째값 = სტრიქონი_მონაცემები; while (항목수--) *첫째값++ = *둘째값++; return მიმართულება_მონაცემები; }
