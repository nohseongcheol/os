#include "../명명/기계연결이름.h"
#include "호출.h"
typedef void (*초기화함수)(void);
extern 초기화함수 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int শুরু_ব্যবহারকারী_অ্যাপ(int);
int ব্যবহারকারী_শুরু(int 전달값) {
    for (초기화함수 *ডাটা_পদ = __init_array_start; ডাটা_পদ < __init_array_end; ডাটা_পদ++) (*ডাটা_পদ)();
    int পরিমাপ = শুরু_ব্যবহারকারী_অ্যাপ(전달값);
    for (초기화함수 *ডাটা_পদ = __fini_array_end; ডাটা_পদ != __fini_array_start;) (*--ডাটা_পদ)();
    return পরিমাপ;
}
void *memset(void *ডাটা_পদ, int মান, size_t 항목수) { unsigned char *গন্তব্য_ডাটা = ডাটা_পদ; while (항목수--) *গন্তব্য_ডাটা++ = মান; return ডাটা_পদ; }
void *memcpy(void *গন্তব্য_ডাটা, const void *স্ট্রিং_ডাটা, size_t 항목수) { unsigned char *첫째값 = গন্তব্য_ডাটা; const unsigned char *둘째값 = স্ট্রিং_ডাটা; while (항목수--) *첫째값++ = *둘째값++; return গন্তব্য_ডাটা; }
