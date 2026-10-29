#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_foydalanuvchi_ilova(int);
int foydalanuvchi_Start(int 전달값) {
    for (초기화함수 *ma_lumotlar_holat = __init_array_start; ma_lumotlar_holat < __init_array_end; ma_lumotlar_holat++) (*ma_lumotlar_holat)();
    int o_lchov = Start_foydalanuvchi_ilova(전달값);
    for (초기화함수 *ma_lumotlar_holat = __fini_array_end; ma_lumotlar_holat != __fini_array_start;) (*--ma_lumotlar_holat)();
    return o_lchov;
}
void *memset(void *ma_lumotlar_holat, int VALUE, size_t kiritish_COUNT) { unsigned char *ko_chirish_joyi_ma_lumotlar = ma_lumotlar_holat; while (kiritish_COUNT--) *ko_chirish_joyi_ma_lumotlar++ = VALUE; return ma_lumotlar_holat; }
void *memcpy(void *ko_chirish_joyi_ma_lumotlar, const void *satr_ma_lumotlar, size_t kiritish_COUNT) { unsigned char *첫째값 = ko_chirish_joyi_ma_lumotlar; const unsigned char *SECOND_VALUE = satr_ma_lumotlar; while (kiritish_COUNT--) *첫째값++ = *SECOND_VALUE++; return ko_chirish_joyi_ma_lumotlar; }
