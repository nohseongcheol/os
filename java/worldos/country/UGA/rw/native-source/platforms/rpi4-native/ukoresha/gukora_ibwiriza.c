#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Itangira_ukoresha_porogaramu(int);
int ukoresha_Itangira(int 전달값) {
    for (초기화함수 *자료위치 = __init_array_start; 자료위치 < __init_array_end; 자료위치++) (*자료위치)();
    int 결과 = Itangira_ukoresha_porogaramu(전달값);
    for (초기화함수 *자료위치 = __fini_array_end; 자료위치 != __fini_array_start;) (*--자료위치)();
    return 결과;
}
void *memset(void *자료위치, int agaciro, size_t 항목수) { unsigned char *aho_ijya_amakurushingiro = 자료위치; while (항목수--) *aho_ijya_amakurushingiro++ = agaciro; return 자료위치; }
void *memcpy(void *aho_ijya_amakurushingiro, const void *igicenteruro_amakurushingiro, size_t 항목수) { unsigned char *첫째값 = aho_ijya_amakurushingiro; const unsigned char *둘째값 = igicenteruro_amakurushingiro; while (항목수--) *첫째값++ = *둘째값++; return aho_ijya_amakurushingiro; }
