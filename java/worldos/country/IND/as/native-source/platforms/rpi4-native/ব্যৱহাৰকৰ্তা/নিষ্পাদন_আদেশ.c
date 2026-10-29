#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্(int);
int ব্যৱহাৰকৰ্তা_আৰম্ভ(int 전달값) {
    for (초기화함수 *ডাটা_স্থান_সলনি_কৰক = __init_array_start; ডাটা_স্থান_সলনি_কৰক < __init_array_end; ডাটা_স্থান_সলনি_কৰক++) (*ডাটা_স্থান_সলনি_কৰক)();
    int পৰিমাপ = আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্(전달값);
    for (초기화함수 *ডাটা_স্থান_সলনি_কৰক = __fini_array_end; ডাটা_স্থান_সলনি_কৰক != __fini_array_start;) (*--ডাটা_স্থান_সলনি_কৰক)();
    return পৰিমাপ;
}
void *memset(void *ডাটা_স্থান_সলনি_কৰক, int মান, size_t 항목수) { unsigned char *গন্তব্য_স্থান_ডাটা = ডাটা_স্থান_সলনি_কৰক; while (항목수--) *গন্তব্য_স্থান_ডাটা++ = মান; return ডাটা_স্থান_সলনি_কৰক; }
void *memcpy(void *গন্তব্য_স্থান_ডাটা, const void *ষ্ট্ৰিং_ডাটা, size_t 항목수) { unsigned char *첫째값 = গন্তব্য_স্থান_ডাটা; const unsigned char *둘째값 = ষ্ট্ৰিং_ডাটা; while (항목수--) *첫째값++ = *둘째값++; return গন্তব্য_স্থান_ডাটা; }
