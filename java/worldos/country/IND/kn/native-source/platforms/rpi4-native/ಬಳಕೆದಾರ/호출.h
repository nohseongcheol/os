#ifndef 자체사용자호출머리
#define 자체사용자호출머리
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 ಪದಸೂಚಿ, x0..x5=인수, x0=ಮಾಪನ/음수 ದೋಷ. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t ಪದಸೂಚಿ, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t 저장기영 __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = ಪದಸೂಚಿ;
    __asm__ volatile("svc #0" : "+r"(저장기영) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)저장기영;
}
static inline intptr_t 화면사각형(unsigned x_ಸಮಭಾಜಕ, unsigned Y_ಬಟನ್_ಸಮನ್ವಯ, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, x_ಸಮಭಾಜಕ, Y_ಬಟನ್_ಸಮನ್ವಯ, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t ಬಳಕೆದಾರ_ಮೆಮೊರಿ_ಅಂತ್ಯಗೊಳಿಸು(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t ಮಾಪನ = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (ಮಾಪನ < 0) return ಮಾಪನ;
    do { ಮಾಪನ = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (ಮಾಪನ == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return ಮಾಪನ;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t ಬಳಕೆದಾರ_ವಾದ(unsigned ಪದಸೂಚಿ, char *ವಿಷಯ_ಮೌಲ್ಯ, size_t ಗಾತ್ರ) {
    return 사용자호출(15, ಪದಸೂಚಿ, (uintptr_t)ವಿಷಯ_ಮೌಲ್ಯ, ಗಾತ್ರ, 0, 0, 0);
}
#endif
