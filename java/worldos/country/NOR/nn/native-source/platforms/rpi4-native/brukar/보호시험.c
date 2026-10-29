#include "호출.h"
extern void _start(void);
int START_brukar_app(int kategori_VALUE) {
    switch (kategori_VALUE) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kjerne_VALUE Skriv
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Skriv
    case 2: { // NX stack Utfør_kommando
        volatile unsigned instruksjon_VALUE = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&instruksjon_VALUE)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Les
    case 7: __asm__ volatile("br xzr"); break; // kjerne_VALUE/NULL Utfør_kommando
    }
    return 99;
}
