#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int);
int aṣàmúlò_bẹ̀rẹ̀(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int iye, size_t 항목수) { unsigned char *èbúté_détà = 자료위치; while (항목수--) *èbúté_détà++ = iye; return 자료위치; }
void *memcpy(void *èbúté_détà, const void *fọ́nrán_détà, size_t 항목수) { unsigned char *첫째값 = èbúté_détà; const unsigned char *둘째값 = fọ́nrán_détà; while (항목수--) *첫째값++ = *둘째값++; return èbúté_détà; }
