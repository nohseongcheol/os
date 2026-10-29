#ifndef собственный_пользователь_вызов_Заголовок
#define собственный_пользователь_вызов_Заголовок
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 ИНДЕКС, x0..x5=аргументы, x0=результат/음수 ошибка. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t ИНДЕКС, uintptr_t 가, uintptr_t СЕКУНДЫ_операнд, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t регистр_нуль __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = СЕКУНДЫ_операнд;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = ИНДЕКС;
    __asm__ volatile("svc #0" : "+r"(регистр_нуль) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)регистр_нуль;
}
static inline intptr_t экран_прямоугольник(unsigned координата_X, unsigned Y_координата, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, координата_X, Y_координата, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t пользователь_Память_элемент(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t результат = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (результат < 0) return результат;
    do { результат = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (результат == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return результат;
}
static inline intptr_t пользователь_аргумент_СЧЁТ(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t пользователь_аргумент(unsigned ИНДЕКС, char *контент_ЗНАЧЕН, size_t Размер) {
    return 사용자호출(15, ИНДЕКС, (uintptr_t)контент_ЗНАЧЕН, Размер, 0, 0, 0);
}
#endif
