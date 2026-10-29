#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન(int);
int ઉપયોગકર્તા_પ્રારંભ(int 전달값) {
    for (초기화함수 *ડેટા_સ્થિતિ = __init_array_start; ડેટા_સ્થિતિ < __init_array_end; ડેટા_સ્થિતિ++) (*ડેટા_સ્થિતિ)();
    int પરિમાણ = પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન(전달값);
    for (초기화함수 *ડેટા_સ્થિતિ = __fini_array_end; ડેટા_સ્થિતિ != __fini_array_start;) (*--ડેટા_સ્થિતિ)();
    return પરિમાણ;
}
void *memset(void *ડેટા_સ્થિતિ, int મૂલ્ય, size_t 항목수) { unsigned char *ગંતવ્ય_ડેટા = ડેટા_સ્થિતિ; while (항목수--) *ગંતવ્ય_ડેટા++ = મૂલ્ય; return ડેટા_સ્થિતિ; }
void *memcpy(void *ગંતવ્ય_ડેટા, const void *સ્ટ્રિંગ_ડેટા, size_t 항목수) { unsigned char *첫째값 = ગંતવ્ય_ડેટા; const unsigned char *둘째값 = સ્ટ્રિંગ_ડેટા; while (항목수--) *첫째값++ = *둘째값++; return ગંતવ્ય_ડેટા; }
