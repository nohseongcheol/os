#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int simolola_modirisi_Tiriso(int);
int modirisi_simolola(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = simolola_modirisi_Tiriso(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int Boleng, size_t 항목수) { unsigned char *bogorogelo_tshedimosetso = 자료위치; while (항목수--) *bogorogelo_tshedimosetso++ = Boleng; return 자료위치; }
void *memcpy(void *bogorogelo_tshedimosetso, const void *dikwalwa_tshedimosetso, size_t 항목수) { unsigned char *첫째값 = bogorogelo_tshedimosetso; const unsigned char *둘째값 = dikwalwa_tshedimosetso; while (항목수--) *첫째값++ = *둘째값++; return bogorogelo_tshedimosetso; }
