#ifndef nativní_uživatel_VOLAT_Nadpis
#define nativní_uživatel_VOLAT_Nadpis
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEX, x0..x5=argumenty, x0=VÝSLEDEK/음수 chyba. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEX, uintptr_t 가, uintptr_t SEKUNDA_operand, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t registr_nula __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SEKUNDA_operand;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEX;
    __asm__ volatile("svc #0" : "+r"(registr_nula) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)registr_nula;
}
static inline intptr_t 화면사각형(unsigned souřadnice_x, unsigned Y_souřadnice, unsigned 너비값, unsigned vyžádáno_výška_HODNOTA, unsigned 빛삼원색) {
    return 사용자호출(13, souřadnice_x, Y_souřadnice, 빛삼원색, 너비값, vyžádáno_výška_HODNOTA, 0);
}
static inline intptr_t uživatel_Paměť_konec(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t VÝSLEDEK = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (VÝSLEDEK < 0) return VÝSLEDEK;
    do { VÝSLEDEK = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (VÝSLEDEK == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return VÝSLEDEK;
}
static inline intptr_t uživatel_argument_POČET(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t uživatel_argument(unsigned INDEX, char *Obsah_HODNOTA, size_t Velikost) {
    return 사용자호출(15, INDEX, (uintptr_t)Obsah_HODNOTA, Velikost, 0, 0, 0);
}
#endif
