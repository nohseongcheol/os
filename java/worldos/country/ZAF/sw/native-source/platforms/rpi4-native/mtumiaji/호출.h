#ifndef 자체사용자호출머리
#define 자체사용자호출머리
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 kielezo, x0..x5=인수, x0=결과/음수 kosa. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t kielezo, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t 저장기영 __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = kielezo;
    __asm__ volatile("svc #0" : "+r"(저장기영) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)저장기영;
}
static inline intptr_t 화면사각형(unsigned jira_x, unsigned Kitufe_cha_Y_kiratibu, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, jira_x, Kitufe_cha_Y_kiratibu, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t mtumiaji_kumbukumbu_tamatia(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t 결과 = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (결과 < 0) return 결과;
    do { 결과 = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (결과 == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return 결과;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t mtumiaji_hoja(unsigned kielezo, char *maudhui_thamani, size_t panga_ukubwa) {
    return 사용자호출(15, kielezo, (uintptr_t)maudhui_thamani, panga_ukubwa, 0, 0, 0);
}
#endif
