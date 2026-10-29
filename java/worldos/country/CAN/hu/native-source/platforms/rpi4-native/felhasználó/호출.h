#ifndef natív_felhasználó_hív_fejléc
#define natív_felhasználó_hív_fejléc
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEX, x0..x5=Argumentumok, x0=KR/음수 HIBA. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEX, uintptr_t 가, uintptr_t MPERC_operandus, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t jegyzék_nulla __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = MPERC_operandus;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEX;
    __asm__ volatile("svc #0" : "+r"(jegyzék_nulla) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)jegyzék_nulla;
}
static inline intptr_t 화면사각형(unsigned x_koordináta, unsigned Y_koordináta, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, x_koordináta, Y_koordináta, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t felhasználó_Memória_megszüntet(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t KR = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (KR < 0) return KR;
    do { KR = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (KR == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return KR;
}
static inline intptr_t felhasználó_argumentum_DARAB(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t felhasználó_argumentum(unsigned INDEX, char *Tartalom_ÉRTÉK, size_t Méret) {
    return 사용자호출(15, INDEX, (uintptr_t)Tartalom_ÉRTÉK, Méret, 0, 0, 0);
}
#endif
