#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_cleachdaiche_ap(int);
int cleachdaiche_Start(int 전달값) {
    for (초기화함수 *dàta_suidhich = __init_array_start; dàta_suidhich < __init_array_end; dàta_suidhich++) (*dàta_suidhich)();
    int tomhas = Start_cleachdaiche_ap(전달값);
    for (초기화함수 *dàta_suidhich = __fini_array_end; dàta_suidhich != __fini_array_start;) (*--dàta_suidhich)();
    return tomhas;
}
void *memset(void *dàta_suidhich, int VALUE, size_t cur_a_steach_COUNT) { unsigned char *ceann_uidhe_dàta = dàta_suidhich; while (cur_a_steach_COUNT--) *ceann_uidhe_dàta++ = VALUE; return dàta_suidhich; }
void *memcpy(void *ceann_uidhe_dàta, const void *sreang_dàta, size_t cur_a_steach_COUNT) { unsigned char *첫째값 = ceann_uidhe_dàta; const unsigned char *SECOND_VALUE = sreang_dàta; while (cur_a_steach_COUNT--) *첫째값++ = *SECOND_VALUE++; return ceann_uidhe_dàta; }
