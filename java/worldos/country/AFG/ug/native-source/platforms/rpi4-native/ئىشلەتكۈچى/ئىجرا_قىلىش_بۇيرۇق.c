#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int باشلاش_ئىشلەتكۈچى_ئەپ(int);
int ئىشلەتكۈچى_باشلاش(int 전달값) {
    for (초기화함수 *مەلۇمات_ئورۇنلاشتۇرۇش = __init_array_start; مەلۇمات_ئورۇنلاشتۇرۇش < __init_array_end; مەلۇمات_ئورۇنلاشتۇرۇش++) (*مەلۇمات_ئورۇنلاشتۇرۇش)();
    int ئۆلچەم = باشلاش_ئىشلەتكۈچى_ئەپ(전달값);
    for (초기화함수 *مەلۇمات_ئورۇنلاشتۇرۇش = __fini_array_end; مەلۇمات_ئورۇنلاشتۇرۇش != __fini_array_start;) (*--مەلۇمات_ئورۇنلاشتۇرۇش)();
    return ئۆلچەم;
}
void *memset(void *مەلۇمات_ئورۇنلاشتۇرۇش, int قىممىتى, size_t 항목수) { unsigned char *نىشان_مەلۇمات = مەلۇمات_ئورۇنلاشتۇرۇش; while (항목수--) *نىشان_مەلۇمات++ = قىممىتى; return مەلۇمات_ئورۇنلاشتۇرۇش; }
void *memcpy(void *نىشان_مەلۇمات, const void *ھەرپ_تىزمىسى_مەلۇمات, size_t 항목수) { unsigned char *첫째값 = نىشان_مەلۇمات; const unsigned char *둘째값 = ھەرپ_تىزمىسى_مەلۇمات; while (항목수--) *첫째값++ = *둘째값++; return نىشان_مەلۇمات; }
