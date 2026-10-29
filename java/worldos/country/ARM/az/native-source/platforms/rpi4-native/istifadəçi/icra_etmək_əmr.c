#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Başla_istifadəçi_proqram(int);
int istifadəçi_Başla(int 전달값) {
    for (초기화함수 *verilənlər_yerinə_qoymaq = __init_array_start; verilənlər_yerinə_qoymaq < __init_array_end; verilənlər_yerinə_qoymaq++) (*verilənlər_yerinə_qoymaq)();
    int ölçü = Başla_istifadəçi_proqram(전달값);
    for (초기화함수 *verilənlər_yerinə_qoymaq = __fini_array_end; verilənlər_yerinə_qoymaq != __fini_array_start;) (*--verilənlər_yerinə_qoymaq)();
    return ölçü;
}
void *memset(void *verilənlər_yerinə_qoymaq, int VALUE, size_t daxiletmə_COUNT) { unsigned char *təyinat_verilənlər = verilənlər_yerinə_qoymaq; while (daxiletmə_COUNT--) *təyinat_verilənlər++ = VALUE; return verilənlər_yerinə_qoymaq; }
void *memcpy(void *təyinat_verilənlər, const void *sətir_verilənlər, size_t daxiletmə_COUNT) { unsigned char *첫째값 = təyinat_verilənlər; const unsigned char *SECOND_VALUE = sətir_verilənlər; while (daxiletmə_COUNT--) *첫째값++ = *SECOND_VALUE++; return təyinat_verilənlər; }
