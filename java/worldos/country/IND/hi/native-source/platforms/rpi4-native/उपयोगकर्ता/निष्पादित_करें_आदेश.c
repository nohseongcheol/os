#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int प्रारंभ_उपयोगकर्ता_ऐप(int);
int उपयोगकर्ता_प्रारंभ(int 전달값) {
    for (초기화함수 *डेटा_पद = __init_array_start; डेटा_पद < __init_array_end; डेटा_पद++) (*डेटा_पद)();
    int परिणाम = प्रारंभ_उपयोगकर्ता_ऐप(전달값);
    for (초기화함수 *डेटा_पद = __fini_array_end; डेटा_पद != __fini_array_start;) (*--डेटा_पद)();
    return परिणाम;
}
void *memset(void *डेटा_पद, int मान, size_t 항목수) { unsigned char *गंतव्य_डेटा = डेटा_पद; while (항목수--) *गंतव्य_डेटा++ = मान; return डेटा_पद; }
void *memcpy(void *गंतव्य_डेटा, const void *स्ट्रिंग_डेटा, size_t 항목수) { unsigned char *첫째값 = गंतव्य_डेटा; const unsigned char *둘째값 = स्ट्रिंग_डेटा; while (항목수--) *첫째값++ = *둘째값++; return गंतव्य_डेटा; }
