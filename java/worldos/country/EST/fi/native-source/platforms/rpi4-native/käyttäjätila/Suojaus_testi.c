#include "호출.h"
extern void _start(void);
int alku_käyttäjä_ohjelma(int alue_ARVO) {
    switch (alue_ARVO) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ydin_ARVO Kirjoitus
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Kirjoitus
    case 2: { // NX stack Suorita_komento
        volatile unsigned käsky_ARVO = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&käsky_ARVO)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Luku
    case 7: __asm__ volatile("br xzr"); break; // ydin_ARVO/NULL Suorita_komento
    }
    return 99;
}
