#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int pigiarli_atuqtuq_pilirijjut(int);
int atuqtuq_pigiarli(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = pigiarli_atuqtuq_pilirijjut(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int atuutilik, size_t 항목수) { unsigned char *namunngarvik_titiqqat = 자료위치; while (항목수--) *namunngarvik_titiqqat++ = atuutilik; return 자료위치; }
void *memcpy(void *namunngarvik_titiqqat, const void *qimiaq_titiqqat, size_t 항목수) { unsigned char *첫째값 = namunngarvik_titiqqat; const unsigned char *둘째값 = qimiaq_titiqqat; while (항목수--) *첫째값++ = *둘째값++; return namunngarvik_titiqqat; }
