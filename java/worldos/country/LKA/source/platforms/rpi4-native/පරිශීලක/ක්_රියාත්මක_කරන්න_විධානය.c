#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ඇරඹුම_පරිශීලක_යෙදු(int);
int පරිශීලක_ඇරඹුම(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = ඇරඹුම_පරිශීලක_යෙදු(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int අගය, size_t 항목수) { unsigned char *ගමනාන්තය_දත්ත = 자료위치; while (항목수--) *ගමනාන්තය_දත්ත++ = අගය; return 자료위치; }
void *memcpy(void *ගමනාන්තය_දත්ත, const void *අනුලකුණු_වැල_දත්ත, size_t 항목수) { unsigned char *첫째값 = ගමනාන්තය_දත්ත; const unsigned char *둘째값 = අනුලකුණු_වැල_දත්ත; while (항목수--) *첫째값++ = *둘째값++; return ගමනාන්තය_දත්ත; }
