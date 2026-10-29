#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int Մեկնարկ_օգտվող_ծրագիր(int);
int օգտվող_Մեկնարկ(int 전달값) {
    for (초기화함수 *տվյալ_դիրք = __init_array_start; տվյալ_դիրք < __init_array_end; տվյալ_դիրք++) (*տվյալ_դիրք)();
    int չափ = Մեկնարկ_օգտվող_ծրագիր(전달값);
    for (초기화함수 *տվյալ_դիրք = __fini_array_end; տվյալ_դիրք != __fini_array_start;) (*--տվյալ_դիրք)();
    return չափ;
}
void *memset(void *տվյալ_դիրք, int արժեք, size_t 항목수) { unsigned char *նպատակակետ_տվյալ = տվյալ_դիրք; while (항목수--) *նպատակակետ_տվյալ++ = արժեք; return տվյալ_դիրք; }
void *memcpy(void *նպատակակետ_տվյալ, const void *տող_տվյալ, size_t 항목수) { unsigned char *첫째값 = նպատակակետ_տվյալ; const unsigned char *둘째값 = տող_տվյալ; while (항목수--) *첫째값++ = *둘째값++; return նպատակակետ_տվյալ; }
