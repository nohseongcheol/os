#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ផ្តើម_អ្នកប្រើ_កម្មវិធី(int);
int អ្នកប្រើ_ផ្តើម(int 전달값) {
    for (초기화함수 *ទិន្នន័យ_កំណត់ទីតាំង = __init_array_start; ទិន្នន័យ_កំណត់ទីតាំង < __init_array_end; ទិន្នន័យ_កំណត់ទីតាំង++) (*ទិន្នន័យ_កំណត់ទីតាំង)();
    int ការវាស់វែង = ផ្តើម_អ្នកប្រើ_កម្មវិធី(전달값);
    for (초기화함수 *ទិន្នន័យ_កំណត់ទីតាំង = __fini_array_end; ទិន្នន័យ_កំណត់ទីតាំង != __fini_array_start;) (*--ទិន្នន័យ_កំណត់ទីតាំង)();
    return ការវាស់វែង;
}
void *memset(void *ទិន្នន័យ_កំណត់ទីតាំង, int តំលៃ, size_t 항목수) { unsigned char *ទិសដៅ_ទិន្នន័យ = ទិន្នន័យ_កំណត់ទីតាំង; while (항목수--) *ទិសដៅ_ទិន្នន័យ++ = តំលៃ; return ទិន្នន័យ_កំណត់ទីតាំង; }
void *memcpy(void *ទិសដៅ_ទិន្នន័យ, const void *សំនុំអក្សរ_ទិន្នន័យ, size_t 항목수) { unsigned char *첫째값 = ទិសដៅ_ទិន្នន័យ; const unsigned char *둘째값 = សំនុំអក្សរ_ទិន្នន័យ; while (항목수--) *첫째값++ = *둘째값++; return ទិសដៅ_ទិន្នន័យ; }
