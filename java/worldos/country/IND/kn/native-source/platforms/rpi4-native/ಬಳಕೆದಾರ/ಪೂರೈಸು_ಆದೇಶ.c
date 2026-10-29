#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(int);
int ಬಳಕೆದಾರ_ಆರಂಭಿಸು(int 전달값) {
    for (초기화함수 *ಡೇಟಾ_ಹುದ್ದೆ = __init_array_start; ಡೇಟಾ_ಹುದ್ದೆ < __init_array_end; ಡೇಟಾ_ಹುದ್ದೆ++) (*ಡೇಟಾ_ಹುದ್ದೆ)();
    int ಮಾಪನ = ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(전달값);
    for (초기화함수 *ಡೇಟಾ_ಹುದ್ದೆ = __fini_array_end; ಡೇಟಾ_ಹುದ್ದೆ != __fini_array_start;) (*--ಡೇಟಾ_ಹುದ್ದೆ)();
    return ಮಾಪನ;
}
void *memset(void *ಡೇಟಾ_ಹುದ್ದೆ, int ಮೌಲ್ಯ, size_t 항목수) { unsigned char *ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ = ಡೇಟಾ_ಹುದ್ದೆ; while (항목수--) *ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ++ = ಮೌಲ್ಯ; return ಡೇಟಾ_ಹುದ್ದೆ; }
void *memcpy(void *ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ, const void *ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ, size_t 항목수) { unsigned char *첫째값 = ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ; const unsigned char *둘째값 = ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ; while (항목수--) *첫째값++ = *둘째값++; return ಗಮ್ಯಸ್ಥಾನ_ಡೇಟಾ; }
