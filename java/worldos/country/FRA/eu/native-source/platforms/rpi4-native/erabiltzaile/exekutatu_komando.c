#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int HASI_erabiltzaile_aplik(int);
int erabiltzaile_HASI(int 전달값) {
    for (초기화함수 *datuak_kargu = __init_array_start; datuak_kargu < __init_array_end; datuak_kargu++) (*datuak_kargu)();
    int EMAITZA = HASI_erabiltzaile_aplik(전달값);
    for (초기화함수 *datuak_kargu = __fini_array_end; datuak_kargu != __fini_array_start;) (*--datuak_kargu)();
    return EMAITZA;
}
void *memset(void *datuak_kargu, int balio, size_t sarrera_ZENBATU) { unsigned char *helburu_datuak = datuak_kargu; while (sarrera_ZENBATU--) *helburu_datuak++ = balio; return datuak_kargu; }
void *memcpy(void *helburu_datuak, const void *kate_datuak, size_t sarrera_ZENBATU) { unsigned char *첫째값 = helburu_datuak; const unsigned char *SEGUNDOA_balio = kate_datuak; while (sarrera_ZENBATU--) *첫째값++ = *SEGUNDOA_balio++; return helburu_datuak; }
