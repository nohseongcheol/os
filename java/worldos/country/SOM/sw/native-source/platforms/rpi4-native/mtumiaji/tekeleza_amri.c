#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Anza_mtumiaji_programu(int);
int mtumiaji_Anza(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Anza_mtumiaji_programu(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int thamani, size_t 항목수) { unsigned char *fikio_data = 자료위치; while (항목수--) *fikio_data++ = thamani; return 자료위치; }
void *memcpy(void *fikio_data, const void *tungo_data, size_t 항목수) { unsigned char *첫째값 = fikio_data; const unsigned char *둘째값 = tungo_data; while (항목수--) *첫째값++ = *둘째값++; return fikio_data; }
