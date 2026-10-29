#ifndef 자체사용자호출머리
#define 자체사용자호출머리
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 اشاریہ, x0..x5=دلائل, x0=پیمائش/음수 غلطی. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t اشاریہ, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t 저장기영 __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = اشاریہ;
    __asm__ volatile("svc #0" : "+r"(저장기영) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)저장기영;
}
static inline intptr_t 화면사각형(unsigned ایکس_مربوط, unsigned 세로좌표, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, ایکس_مربوط, 세로좌표, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t صارف_میموری_اختتام(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t پیمائش = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (پیمائش < 0) return پیمائش;
    do { پیمائش = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (پیمائش == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return پیمائش;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t صارف_دلائل(unsigned اشاریہ, char *مشمول_قدر, size_t حجم) {
    return 사용자호출(15, اشاریہ, (uintptr_t)مشمول_قدر, حجم, 0, 0, 0);
}
#endif
