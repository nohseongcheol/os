#include "호출.h"
extern void _start(void);
int ਸੁਰੂ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(int ਸ਼੍ਰੇਣੀ_ਕੀਮਤ) {
    switch (ਸ਼੍ਰੇਣੀ_ਕੀਮਤ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ ਲਿਖਣ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ਲਿਖਣ
    case 2: { // NX stack ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼
        volatile unsigned ਨਿਰਦੇਸ਼_ਕੀਮਤ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ਨਿਰਦੇਸ਼_ਕੀਮਤ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 ਪੜ੍ਹਨ
    case 7: __asm__ volatile("br xzr"); break; // ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ/NULL ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼
    }
    return 99;
}
