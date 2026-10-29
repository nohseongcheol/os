#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int басы_пайдаланушы_бағдарлама(int);
int пайдаланушы_басы(int 전달값) {
    for (초기화함수 *деректер_лауазым = __init_array_start; деректер_лауазым < __init_array_end; деректер_лауазым++) (*деректер_лауазым)();
    int НӘТИЖЕ = басы_пайдаланушы_бағдарлама(전달값);
    for (초기화함수 *деректер_лауазым = __fini_array_end; деректер_лауазым != __fini_array_start;) (*--деректер_лауазым)();
    return НӘТИЖЕ;
}
void *memset(void *деректер_лауазым, int мән, size_t 항목수) { unsigned char *тағайындау_деректер = деректер_лауазым; while (항목수--) *тағайындау_деректер++ = мән; return деректер_лауазым; }
void *memcpy(void *тағайындау_деректер, const void *жол_деректер, size_t 항목수) { unsigned char *첫째값 = тағайындау_деректер; const unsigned char *둘째값 = жол_деректер; while (항목수--) *첫째값++ = *둘째값++; return тағайындау_деректер; }
