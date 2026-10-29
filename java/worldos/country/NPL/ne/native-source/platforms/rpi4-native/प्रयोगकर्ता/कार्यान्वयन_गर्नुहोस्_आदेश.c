#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int सुरु_प्रयोगकर्ता_अनुप्रयोग(int);
int प्रयोगकर्ता_सुरु(int 전달값) {
    for (초기화함수 *लगत_राख्नुहोस् = __init_array_start; लगत_राख्नुहोस् < __init_array_end; लगत_राख्नुहोस्++) (*लगत_राख्नुहोस्)();
    int मापन = सुरु_प्रयोगकर्ता_अनुप्रयोग(전달값);
    for (초기화함수 *लगत_राख्नुहोस् = __fini_array_end; लगत_राख्नुहोस् != __fini_array_start;) (*--लगत_राख्नुहोस्)();
    return मापन;
}
void *memset(void *लगत_राख्नुहोस्, int मान, size_t 항목수) { unsigned char *गन्तव्य_लगत = लगत_राख्नुहोस्; while (항목수--) *गन्तव्य_लगत++ = मान; return लगत_राख्नुहोस्; }
void *memcpy(void *गन्तव्य_लगत, const void *स्ट्रिङ_लगत, size_t 항목수) { unsigned char *첫째값 = गन्तव्य_लगत; const unsigned char *둘째값 = स्ट्रिङ_लगत; while (항목수--) *첫째값++ = *둘째값++; return गन्तव्य_लगत; }
