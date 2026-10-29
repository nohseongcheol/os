#ifndef 자체사용자호출머리
#define 자체사용자호출머리
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 INDEX, x0..x5=Argumendid, x0=TULEMUS/음수 VIGA. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t INDEX, uintptr_t 가, uintptr_t SECOND_operand, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t register_null __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SECOND_operand;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = INDEX;
    __asm__ volatile("svc #0" : "+r"(register_null) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)register_null;
}
static inline intptr_t 화면사각형(unsigned 가로좌표, unsigned 세로좌표, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, 가로좌표, 세로좌표, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t kasutaja_Mälu_lõpeta_kõne(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t TULEMUS = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (TULEMUS < 0) return TULEMUS;
    do { TULEMUS = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (TULEMUS == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return TULEMUS;
}
static inline intptr_t kasutaja_argument_COUNT(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t kasutaja_argument(unsigned INDEX, char *Sisu_VALUE, size_t Suurus) {
    return 사용자호출(15, INDEX, (uintptr_t)Sisu_VALUE, Suurus, 0, 0, 0);
}
#endif
