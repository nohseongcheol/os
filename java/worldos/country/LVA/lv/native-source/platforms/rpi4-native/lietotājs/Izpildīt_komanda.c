#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Sākt_lietotājs_programma(int);
int lietotājs_Sākt(int 전달값) {
    for (초기화함수 *dati_amats = __init_array_start; dati_amats < __init_array_end; dati_amats++) (*dati_amats)();
    int mērs = Sākt_lietotājs_programma(전달값);
    for (초기화함수 *dati_amats = __fini_array_end; dati_amats != __fini_array_start;) (*--dati_amats)();
    return mērs;
}
void *memset(void *dati_amats, int VALUE, size_t ievade_COUNT) { unsigned char *mērķis_dati = dati_amats; while (ievade_COUNT--) *mērķis_dati++ = VALUE; return dati_amats; }
void *memcpy(void *mērķis_dati, const void *virkne_dati, size_t ievade_COUNT) { unsigned char *첫째값 = mērķis_dati; const unsigned char *SECOND_VALUE = virkne_dati; while (ievade_COUNT--) *첫째값++ = *SECOND_VALUE++; return mērķis_dati; }
