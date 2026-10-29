#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ጀምር_ተጠቃሚ_መተግበሪ(int);
int ተጠቃሚ_ጀምር(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = ጀምር_ተጠቃሚ_መተግበሪ(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int ዋጋ, size_t 항목수) { unsigned char *መዓልቦ_ሓበሬታ = 자료위치; while (항목수--) *መዓልቦ_ሓበሬታ++ = ዋጋ; return 자료위치; }
void *memcpy(void *መዓልቦ_ሓበሬታ, const void *ሕብረ_ቁምፊ_ሓበሬታ, size_t 항목수) { unsigned char *첫째값 = መዓልቦ_ሓበሬታ; const unsigned char *둘째값 = ሕብረ_ቁምፊ_ሓበሬታ; while (항목수--) *첫째값++ = *둘째값++; return መዓልቦ_ሓበሬታ; }
