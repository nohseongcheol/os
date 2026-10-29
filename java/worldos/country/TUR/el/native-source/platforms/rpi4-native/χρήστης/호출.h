#ifndef εγγενής_χρήστης_καλώ_κεφαλίδα
#define εγγενής_χρήστης_καλώ_κεφαλίδα
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 Ευρετήριο, x0..x5=Παράμετροι, x0=μέτρηση/음수 ΣΦΑΛΜΑ. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t Ευρετήριο, uintptr_t 가, uintptr_t 나, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t δήλωση_μηδέν __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = 나;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = Ευρετήριο;
    __asm__ volatile("svc #0" : "+r"(δήλωση_μηδέν) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)δήλωση_μηδέν;
}
static inline intptr_t 화면사각형(unsigned συντεταγμένη_x, unsigned κουμπί_Y_συντονισμός, unsigned 너비값, unsigned ζητήθηκε_ύψος_τιμή, unsigned 빛삼원색) {
    return 사용자호출(13, συντεταγμένη_x, κουμπί_Y_συντονισμός, 빛삼원색, 너비값, ζητήθηκε_ύψος_τιμή, 0);
}
static inline intptr_t χρήστης_Μνήμη_Τελική_οντότητα(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t μέτρηση = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (μέτρηση < 0) return μέτρηση;
    do { μέτρηση = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (μέτρηση == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return μέτρηση;
}
static inline intptr_t 사용자인수개수(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t χρήστης_όρισμα(unsigned Ευρετήριο, char *Περιεχόμενο_τιμή, size_t Μέγεθος) {
    return 사용자호출(15, Ευρετήριο, (uintptr_t)Περιεχόμενο_τιμή, Μέγεθος, 0, 0, 0);
}
#endif
