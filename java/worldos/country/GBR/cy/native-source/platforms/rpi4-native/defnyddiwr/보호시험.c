#include "호출.h"
extern void _start(void);
int START_defnyddiwr_Rhaglen(int ardal_VALUE) {
    switch (ardal_VALUE) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // cnewyllyn_VALUE Ysgrifennu
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Ysgrifennu
    case 2: { // NX stack Gweithredu_gorchymyn
        volatile unsigned cyfarwyddyd_VALUE = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&cyfarwyddyd_VALUE)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Darllen
    case 7: __asm__ volatile("br xzr"); break; // cnewyllyn_VALUE/NULL Gweithredu_gorchymyn
    }
    return 99;
}
