#ifndef đầuMụcGọiNgườiDùngBảnĐịa
#define đầuMụcGọiNgườiDùngBảnĐịa
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=gọiThựcHiện sốHiệu, x0..x5=cácĐốiSố, x0=kếtQuả/giáTrịÂm lỗi. Linux ABI 아님.
static inline intptr_t gọiThựcHiệnNgườiDùng(uintptr_t sốHiệu, uintptr_t toánHạngĐầuTiên, uintptr_t toánHạngThứHai, uintptr_t toánHạngThứBa,
                                uintptr_t toánHạngThứTư, uintptr_t toánHạngThứNăm, uintptr_t toánHạngThứSáu) {
    register uintptr_t thanhGhiKhôngSố __asm__("x0") = toánHạngĐầuTiên;
    register uintptr_t thanhGhiMột __asm__("x1") = toánHạngThứHai;
    register uintptr_t thanhGhiHai __asm__("x2") = toánHạngThứBa;
    register uintptr_t thanhGhiBa __asm__("x3") = toánHạngThứTư;
    register uintptr_t thanhGhiBốn __asm__("x4") = toánHạngThứNăm;
    register uintptr_t thanhGhiNăm __asm__("x5") = toánHạngThứSáu;
    register uintptr_t thanhGhiTám __asm__("x8") = sốHiệu;
    __asm__ volatile("svc #0" : "+r"(thanhGhiKhôngSố) : "r"(thanhGhiMột), "r"(thanhGhiHai), "r"(thanhGhiBa), "r"(thanhGhiBốn), "r"(thanhGhiNăm), "r"(thanhGhiTám) : "memory", "cc");
    return (intptr_t)thanhGhiKhôngSố;
}
static inline intptr_t hìnhChữNhậtMànHình(unsigned tọaĐộX, unsigned tọaĐộY, unsigned giáTrịRộngĐãYêuCầu, unsigned giáTrịCaoĐãYêuCầu, unsigned màuRGB) {
    return gọiThựcHiệnNgườiDùng(13, tọaĐộX, tọaĐộY, màuRGB, giáTrịRộngĐãYêuCầu, giáTrịCaoĐãYêuCầu, 0);
}
static inline intptr_t kếtThúcBộNhớNgườiDùng(uintptr_t phầnKết) { return gọiThựcHiệnNgườiDùng(8, phầnKết, 0, 0, 0, 0, 0); }
static inline intptr_t đọcRộngMànHình(void) { return gọiThựcHiệnNgườiDùng(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t đọcCaoMànHình(void) { return gọiThựcHiệnNgườiDùng(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t chờPhímMànHìnhCho(void) {
    intptr_t kếtQuả = gọiThựcHiệnNgườiDùng(16, 0, 0, 0, 0, 0, 0);
    if (kếtQuả < 0) return kếtQuả;
    do { kếtQuả = gọiThựcHiệnNgườiDùng(16, 1, 0, 0, 0, 0, 0); } while (kếtQuả == -11);
    gọiThựcHiệnNgườiDùng(16, 2, 0, 0, 0, 0, 0);
    return kếtQuả;
}
static inline intptr_t sốLượngĐốiSốNgườiDùng(void) { return gọiThựcHiệnNgườiDùng(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t đốiSốNgườiDùng(unsigned sốHiệu, char *giáTrịNộiDung, size_t cỡ) {
    return gọiThựcHiệnNgườiDùng(15, sốHiệu, (uintptr_t)giáTrịNộiDung, cỡ, 0, 0, 0);
}
#endif
