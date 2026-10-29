#ifndef alkuperäinen_käyttäjä_KUTSU_otsikko
#define alkuperäinen_käyttäjä_KUTSU_otsikko
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEKSI, x0..x5=argumentit, x0=TULOS/음수 VIRHE. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEKSI, uintptr_t 가, uintptr_t SEKUNNIT_operandi, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t rekisteri_nolla __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SEKUNNIT_operandi;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEKSI;
    __asm__ volatile("svc #0" : "+r"(rekisteri_nolla) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)rekisteri_nolla;
}
static inline intptr_t 화면사각형(unsigned x_koordinaatti, unsigned Y_koordinaatti, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, x_koordinaatti, Y_koordinaatti, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t käyttäjä_Muisti_lopettaa_puhelu(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t TULOS = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (TULOS < 0) return TULOS;
    do { TULOS = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (TULOS == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return TULOS;
}
static inline intptr_t käyttäjä_argumentti_LASKE(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t käyttäjä_argumentti(unsigned INDEKSI, char *Sisältö_ARVO, size_t Koko) {
    return 사용자호출(15, INDEKSI, (uintptr_t)Sisältö_ARVO, Koko, 0, 0, 0);
}
#endif
