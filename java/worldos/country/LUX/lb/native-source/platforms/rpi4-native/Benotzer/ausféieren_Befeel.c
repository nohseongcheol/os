#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_Benotzer_App(int);
int Benotzer_Start(int 전달값) {
    for (초기화함수 *Daten_positionéieren = __init_array_start; Daten_positionéieren < __init_array_end; Daten_positionéieren++) (*Daten_positionéieren)();
    int Mooss = Start_Benotzer_App(전달값);
    for (초기화함수 *Daten_positionéieren = __fini_array_end; Daten_positionéieren != __fini_array_start;) (*--Daten_positionéieren)();
    return Mooss;
}
void *memset(void *Daten_positionéieren, int VALUE, size_t Agab_COUNT) { unsigned char *Zil_Daten = Daten_positionéieren; while (Agab_COUNT--) *Zil_Daten++ = VALUE; return Daten_positionéieren; }
void *memcpy(void *Zil_Daten, const void *Zeechefolleg_Daten, size_t Agab_COUNT) { unsigned char *첫째값 = Zil_Daten; const unsigned char *SECOND_VALUE = Zeechefolleg_Daten; while (Agab_COUNT--) *첫째값++ = *SECOND_VALUE++; return Zil_Daten; }
