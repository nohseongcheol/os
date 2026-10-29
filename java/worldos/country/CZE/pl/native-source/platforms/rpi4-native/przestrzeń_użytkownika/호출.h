#ifndef natywny_użytkownik_Połącz_Nagłówek
#define natywny_użytkownik_Połącz_Nagłówek
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEKS, x0..x5=argumenty, x0=WYNIK/negatywny_WARTOŚĆ błąd. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEKS, uintptr_t 가, uintptr_t SEKUNDA_operand, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t rejestr_zero __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SEKUNDA_operand;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEKS;
    __asm__ volatile("svc #0" : "+r"(rejestr_zero) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)rejestr_zero;
}
static inline intptr_t 화면사각형(unsigned współrzędna_X, unsigned Y_współrzędna, unsigned 너비값, unsigned wymagane_wysokość_WARTOŚĆ, unsigned 빛삼원색) {
    return 사용자호출(13, współrzędna_X, Y_współrzędna, 빛삼원색, 너비값, wymagane_wysokość_WARTOŚĆ, 0);
}
static inline intptr_t użytkownik_Pamięć_Koniec(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t WYNIK = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (WYNIK < 0) return WYNIK;
    do { WYNIK = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (WYNIK == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return WYNIK;
}
static inline intptr_t użytkownik_argument_ILE_LICZB(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t użytkownik_argument(unsigned INDEKS, char *treść_WARTOŚĆ_cb0f2404, size_t Rozmiar) {
    return 사용자호출(15, INDEKS, (uintptr_t)treść_WARTOŚĆ_cb0f2404, Rozmiar, 0, 0, 0);
}
#endif
