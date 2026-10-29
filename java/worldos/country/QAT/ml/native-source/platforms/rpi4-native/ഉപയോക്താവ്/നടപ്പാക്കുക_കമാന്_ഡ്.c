#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം(int);
int ഉപയോക്താവ്_ആരംഭം(int 전달값) {
    for (초기화함수 *ഡാറ്റാ_പദവി = __init_array_start; ഡാറ്റാ_പദവി < __init_array_end; ഡാറ്റാ_പദവി++) (*ഡാറ്റാ_പദവി)();
    int അളവ് = ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം(전달값);
    for (초기화함수 *ഡാറ്റാ_പദവി = __fini_array_end; ഡാറ്റാ_പദവി != __fini_array_start;) (*--ഡാറ്റാ_പദവി)();
    return അളവ്;
}
void *memset(void *ഡാറ്റാ_പദവി, int മൂല്യം, size_t 항목수) { unsigned char *ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ = ഡാറ്റാ_പദവി; while (항목수--) *ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ++ = മൂല്യം; return ഡാറ്റാ_പദവി; }
void *memcpy(void *ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ, const void *സ്ട്രിംഗ്_ഡാറ്റാ, size_t 항목수) { unsigned char *첫째값 = ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ; const unsigned char *둘째값 = സ്ട്രിംഗ്_ഡാറ്റാ; while (항목수--) *첫째값++ = *둘째값++; return ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ; }
