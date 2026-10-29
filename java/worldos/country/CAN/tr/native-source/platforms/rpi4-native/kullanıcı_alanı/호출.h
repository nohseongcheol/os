#ifndef yerel_kullanıcı_Ara_Başlık
#define yerel_kullanıcı_Ara_Başlık
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=호출 Dizin, x0..x5=bağımsız_değişkenler, x0=sonuç/Negatif_değer hata. Linux ABI 아님.
static inline intptr_t 사용자호출(uintptr_t Dizin, uintptr_t 가, uintptr_t SANİYE_işlenen, uintptr_t 다,
                                uintptr_t 라, uintptr_t 마, uintptr_t 바) {
    register uintptr_t yazmaç_sıfır __asm__("x0") = 가;
    register uintptr_t 저장기일 __asm__("x1") = SANİYE_işlenen;
    register uintptr_t 저장기이 __asm__("x2") = 다;
    register uintptr_t 저장기삼 __asm__("x3") = 라;
    register uintptr_t 저장기사 __asm__("x4") = 마;
    register uintptr_t 저장기오 __asm__("x5") = 바;
    register uintptr_t 저장기팔 __asm__("x8") = Dizin;
    __asm__ volatile("svc #0" : "+r"(yazmaç_sıfır) : "r"(저장기일), "r"(저장기이), "r"(저장기삼), "r"(저장기사), "r"(저장기오), "r"(저장기팔) : "memory", "cc");
    return (intptr_t)yazmaç_sıfır;
}
static inline intptr_t 화면사각형(unsigned x_koordinatı, unsigned Y_koordinat, unsigned 너비값, unsigned 높이값, unsigned 빛삼원색) {
    return 사용자호출(13, x_koordinatı, Y_koordinat, 빛삼원색, 너비값, 높이값, 0);
}
static inline intptr_t kullanıcı_Bellek_Bitiş(uintptr_t 끝) { return 사용자호출(8, 끝, 0, 0, 0, 0, 0); }
static inline intptr_t 화면너비읽기(void) { return 사용자호출(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 화면높이읽기(void) { return 사용자호출(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 화면키기다리기(void) {
    intptr_t sonuç = 사용자호출(16, 0, 0, 0, 0, 0, 0);
    if (sonuç < 0) return sonuç;
    do { sonuç = 사용자호출(16, 1, 0, 0, 0, 0, 0); } while (sonuç == -11);
    사용자호출(16, 2, 0, 0, 0, 0, 0);
    return sonuç;
}
static inline intptr_t kullanıcı_bağımsız_değişken_BAĞ_DEĞ_SAY(void) { return 사용자호출(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t kullanıcı_bağımsız_değişken(unsigned Dizin, char *içerik_değer, size_t Boyut) {
    return 사용자호출(15, Dizin, (uintptr_t)içerik_değer, Boyut, 0, 0, 0);
}
#endif
