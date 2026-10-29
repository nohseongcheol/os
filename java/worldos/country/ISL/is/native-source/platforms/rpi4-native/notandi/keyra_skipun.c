#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Opna_notandi_forrit(int);
int notandi_Opna(int 전달값) {
    for (초기화함수 *gögn_staða = __init_array_start; gögn_staða < __init_array_end; gögn_staða++) (*gögn_staða)();
    int NIÐURSTAÐA = Opna_notandi_forrit(전달값);
    for (초기화함수 *gögn_staða = __fini_array_end; gögn_staða != __fini_array_start;) (*--gögn_staða)();
    return NIÐURSTAÐA;
}
void *memset(void *gögn_staða, int VALUE, size_t færsla_COUNT) { unsigned char *endastaður_gögn = gögn_staða; while (færsla_COUNT--) *endastaður_gögn++ = VALUE; return gögn_staða; }
void *memcpy(void *endastaður_gögn, const void *strengur_gögn, size_t færsla_COUNT) { unsigned char *첫째값 = endastaður_gögn; const unsigned char *SECOND_VALUE = strengur_gögn; while (færsla_COUNT--) *첫째값++ = *SECOND_VALUE++; return endastaður_gögn; }
