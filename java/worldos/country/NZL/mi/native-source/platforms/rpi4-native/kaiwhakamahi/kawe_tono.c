#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Start_kaiwhakamahi_kaupapa(int);
int kaiwhakamahi_Start(int 전달값) {
    for (초기화함수 *raraunga_tūranga = __init_array_start; raraunga_tūranga < __init_array_end; raraunga_tūranga++) (*raraunga_tūranga)();
    int mēhua = Start_kaiwhakamahi_kaupapa(전달값);
    for (초기화함수 *raraunga_tūranga = __fini_array_end; raraunga_tūranga != __fini_array_start;) (*--raraunga_tūranga)();
    return mēhua;
}
void *memset(void *raraunga_tūranga, int uara, size_t tāurunga_COUNT) { unsigned char *ūnga_raraunga = raraunga_tūranga; while (tāurunga_COUNT--) *ūnga_raraunga++ = uara; return raraunga_tūranga; }
void *memcpy(void *ūnga_raraunga, const void *aho_raraunga, size_t tāurunga_COUNT) { unsigned char *첫째값 = ūnga_raraunga; const unsigned char *SECOND_uara = aho_raraunga; while (tāurunga_COUNT--) *첫째값++ = *SECOND_uara++; return ūnga_raraunga; }
