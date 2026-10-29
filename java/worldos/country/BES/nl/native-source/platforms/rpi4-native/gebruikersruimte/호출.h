#ifndef systeemeigen_gebruiker_Bellen_header
#define systeemeigen_gebruiker_Bellen_header
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEX, x0..x5=argumenten, x0=resultaat/음수 fout. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEX, uintptr_t 가, uintptr_t SECONDE_operand, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t register_nul __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SECONDE_operand;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEX;
    __asm__ volatile("svc #0" : "+r"(register_nul) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)register_nul;
}
static inline intptr_t scherm_rechthoek(unsigned x_coördinaat, unsigned Y_coördinaat, unsigned 너비값, unsigned aangevraagd_hoogte_WAARDE, unsigned 빛삼원색) {
    return 사용자호출(13, x_coördinaat, Y_coördinaat, 빛삼원색, 너비값, aangevraagd_hoogte_WAARDE, 0);
}
static inline intptr_t gebruiker_Geheugen_beëindigen(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t resultaat = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (resultaat < 0) return resultaat;
    do { resultaat = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (resultaat == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return resultaat;
}
static inline intptr_t gebruiker_argument_AANTAL(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t gebruiker_argument(unsigned INDEX, char *Inhoud_WAARDE, size_t Grootte) {
    return 사용자호출(15, INDEX, (uintptr_t)Inhoud_WAARDE, Grootte, 0, 0, 0);
}
#endif
