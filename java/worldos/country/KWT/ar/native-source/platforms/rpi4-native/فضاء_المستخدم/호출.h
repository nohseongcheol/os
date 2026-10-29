#ifndef أصلي_مستخدم_يتصل_عنوان
#define أصلي_مستخدم_يتصل_عنوان
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 فهرس, x0..x5=وسائط, x0=نتيجة/음수 خطأ. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t فهرس, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t سجل_صفر __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = فهرس;
    __asm__ volatile("svc #0" : "+r"(سجل_صفر) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)سجل_صفر;
}
static inline intptr_t 화면사각형(unsigned الإحداثي_س, unsigned الزر_Y_إحداثيات, unsigned 너비값, unsigned مطلوب_ارتفاع_قيمة, unsigned 빛삼원색) {
    return 사용자호출(13, الإحداثي_س, الزر_Y_إحداثيات, 빛삼원색, 너비값, مطلوب_ارتفاع_قيمة, 0);
}
static inline intptr_t مستخدم_ذاكرة_إنهاء_مكالمة(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t نتيجة = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (نتيجة < 0) return نتيجة;
    do { نتيجة = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (نتيجة == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return نتيجة;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t مستخدم_وسيطة(unsigned فهرس, char *محتوى_قيمة, size_t حجم) {
    return 사용자호출(15, فهرس, (uintptr_t)محتوى_قيمة, حجم, 0, 0, 0);
}
#endif
