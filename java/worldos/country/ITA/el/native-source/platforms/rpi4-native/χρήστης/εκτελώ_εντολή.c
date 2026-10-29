#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int αρχή_χρήστης_εφαρμογή(int);
int χρήστης_αρχή(int 전달값) {
    for (초기화함수 *δεδομένα_θέση = __init_array_start; δεδομένα_θέση < __init_array_end; δεδομένα_θέση++) (*δεδομένα_θέση)();
    int μέτρηση = αρχή_χρήστης_εφαρμογή(전달값);
    for (초기화함수 *δεδομένα_θέση = __fini_array_end; δεδομένα_θέση != __fini_array_start;) (*--δεδομένα_θέση)();
    return μέτρηση;
}
void *memset(void *δεδομένα_θέση, int τιμή, size_t 항목수) { unsigned char *προορισμός_δεδομένα = δεδομένα_θέση; while (항목수--) *προορισμός_δεδομένα++ = τιμή; return δεδομένα_θέση; }
void *memcpy(void *προορισμός_δεδομένα, const void *συμβολοσειρά_δεδομένα, size_t 항목수) { unsigned char *첫째값 = προορισμός_δεδομένα; const unsigned char *둘째값 = συμβολοσειρά_δεδομένα; while (항목수--) *첫째값++ = *둘째값++; return προορισμός_δεδομένα; }
