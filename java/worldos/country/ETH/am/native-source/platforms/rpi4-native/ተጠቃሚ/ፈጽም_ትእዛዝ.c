#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ጀምር_ተጠቃሚ_ፕሮግራም(int);
int ተጠቃሚ_ጀምር(int 전달값) {
    for (초기화함수 *ውሂብ_በቦታ_አስቀመጠ = __init_array_start; ውሂብ_በቦታ_አስቀመጠ < __init_array_end; ውሂብ_በቦታ_አስቀመጠ++) (*ውሂብ_በቦታ_አስቀመጠ)();
    int ልኬት = ጀምር_ተጠቃሚ_ፕሮግራም(전달값);
    for (초기화함수 *ውሂብ_በቦታ_አስቀመጠ = __fini_array_end; ውሂብ_በቦታ_አስቀመጠ != __fini_array_start;) (*--ውሂብ_በቦታ_አስቀመጠ)();
    return ልኬት;
}
void *memset(void *ውሂብ_በቦታ_አስቀመጠ, int እሴት, size_t 항목수) { unsigned char *መድረሻ_ውሂብ = ውሂብ_በቦታ_አስቀመጠ; while (항목수--) *መድረሻ_ውሂብ++ = እሴት; return ውሂብ_በቦታ_አስቀመጠ; }
void *memcpy(void *መድረሻ_ውሂብ, const void *ኅብረቁምፊ_ውሂብ, size_t 항목수) { unsigned char *첫째값 = መድረሻ_ውሂብ; const unsigned char *둘째값 = ኅብረቁምፊ_ውሂብ; while (항목수--) *첫째값++ = *둘째값++; return መድረሻ_ውሂብ; }
