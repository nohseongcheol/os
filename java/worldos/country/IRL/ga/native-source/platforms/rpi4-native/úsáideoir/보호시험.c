#include "호출.h"
extern void _start(void);
int Start_úsáideoir_clár(int catagóir_VALUE) {
    switch (catagóir_VALUE) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // eithne_VALUE Scríobh
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Scríobh
    case 2: { // NX stack Rith_ordú
        volatile unsigned treoir_VALUE = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&treoir_VALUE)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Léigh
    case 7: __asm__ volatile("br xzr"); break; // eithne_VALUE/NULL Rith_ordú
    }
    return 99;
}
