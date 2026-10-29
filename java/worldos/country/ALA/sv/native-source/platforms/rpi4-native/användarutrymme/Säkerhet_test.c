#include "호출.h"
extern void _start(void);
int START_användare_app(int område_värde) {
    switch (område_värde) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kärna_värde Skriv
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Skriv
    case 2: { // NX stack köra_kommando
        volatile unsigned instruktion_värde = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&instruktion_värde)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Läs
    case 7: __asm__ volatile("br xzr"); break; // kärna_värde/NULL köra_kommando
    }
    return 99;
}
