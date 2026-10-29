#ifndef nativo_USER_Chiama_Intestazione
#define nativo_USER_Chiama_Intestazione
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDICE, x0..x5=argomenti, x0=risultato/negativo_VALORE errore. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDICE, uintptr_t 가, uintptr_t SECONDO_operando, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t registro_zero __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SECONDO_operando;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDICE;
    __asm__ volatile("svc #0" : "+r"(registro_zero) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)registro_zero;
}
static inline intptr_t schermata_rettangolo(unsigned coordinata_x, unsigned Y_coordinata, unsigned 너비값, unsigned richiesto_altezza_VALORE, unsigned 빛삼원색) {
    return 사용자호출(13, coordinata_x, Y_coordinata, 빛삼원색, 너비값, richiesto_altezza_VALORE, 0);
}
static inline intptr_t USER_Memoria_chiudere(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t risultato = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (risultato < 0) return risultato;
    do { risultato = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (risultato == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return risultato;
}
static inline intptr_t USER_argomento_CONTA_NUMERI(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t USER_argomento(unsigned INDICE, char *Contenuto_VALORE, size_t Dimensione) {
    return 사용자호출(15, INDICE, (uintptr_t)Contenuto_VALORE, Dimensione, 0, 0, 0);
}
#endif
