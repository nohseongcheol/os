#include "호출.h"
extern void _start(void);
int simolola_modirisi_Tiriso(int setlhopha_Boleng_4b6d6445) {
    switch (setlhopha_Boleng_4b6d6445) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // Khenele_Boleng kwala
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text kwala
    case 2: { // NX stack diragatsa_Taelo
        volatile unsigned taelo_Boleng = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&taelo_Boleng)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // Khenele_Boleng/NULL diragatsa_Taelo
    }
    return 99;
}
