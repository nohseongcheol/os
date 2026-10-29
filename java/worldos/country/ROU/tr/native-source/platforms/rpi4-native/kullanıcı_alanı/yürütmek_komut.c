#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*başlatıcı_metot)(void);
extern başlatıcı_metot __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_kullanıcı_program(int);
int kullanıcı_Start(int 전달값) {
    for (başlatıcı_metot *veri_konum = __init_array_start; veri_konum < __init_array_end; veri_konum++) (*veri_konum)();
    int sonuç = Start_kullanıcı_program(전달값);
    for (başlatıcı_metot *veri_konum = __fini_array_end; veri_konum != __fini_array_start;) (*--veri_konum)();
    return sonuç;
}
void *memset(void *veri_konum, int değer, size_t girdi_BAĞ_DEĞ_SAY) { unsigned char *hedef_veri = veri_konum; while (girdi_BAĞ_DEĞ_SAY--) *hedef_veri++ = değer; return veri_konum; }
void *memcpy(void *hedef_veri, const void *dize_veri, size_t girdi_BAĞ_DEĞ_SAY) { unsigned char *첫째값 = hedef_veri; const unsigned char *SANİYE_değer = dize_veri; while (girdi_BAĞ_DEĞ_SAY--) *첫째값++ = *SANİYE_değer++; return hedef_veri; }
