#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int);
int ᎬᏗᏍᎩ_ᎭᏂᎩᏍᏓ(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int ᏧᎬᏩᎶᏗᏯ, size_t 항목수) { unsigned char *ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ = 자료위치; while (항목수--) *ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ++ = ᏧᎬᏩᎶᏗᏯ; return 자료위치; }
void *memcpy(void *ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ, const void *ᎠᏍᏘ_ᎦᏟᏌᏅᎯ, size_t 항목수) { unsigned char *첫째값 = ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ; const unsigned char *둘째값 = ᎠᏍᏘ_ᎦᏟᏌᏅᎯ; while (항목수--) *첫째값++ = *둘째값++; return ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ; }
