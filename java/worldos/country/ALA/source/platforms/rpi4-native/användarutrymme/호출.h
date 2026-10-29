#ifndef ursprunglig_användare_ring_huvud
#define ursprunglig_användare_ring_huvud
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEX, x0..x5=argument, x0=RESULTAT/음수 fel. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEX, uintptr_t 가, uintptr_t SEKUND_operand, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t register_noll __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SEKUND_operand;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEX;
    __asm__ volatile("svc #0" : "+r"(register_noll) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)register_noll;
}
static inline intptr_t skärmbild_rektangel(unsigned x_koordinat, unsigned Y_koordinat, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, x_koordinat, Y_koordinat, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t användare_Minne_avsluta(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t RESULTAT = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (RESULTAT < 0) return RESULTAT;
    do { RESULTAT = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (RESULTAT == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return RESULTAT;
}
static inline intptr_t användare_argument_ANTAL(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t användare_argument(unsigned INDEX, char *Innehåll_värde, size_t Storlek) {
    return 사용자호출(15, INDEX, (uintptr_t)Innehåll_värde, Storlek, 0, 0, 0);
}
#endif
