#include "호출.h"
extern void _start(void);
int Fara_Mai_anfani_da_kwamfuta_Shiri(int ɓangare_Daraja) {
    switch (ɓangare_Daraja) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // Kwara_Daraja Yi_Rubutu
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Yi_Rubutu
    case 2: { // NX stack gudanar_Umarni
        volatile unsigned Sharadi_Daraja = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&Sharadi_Daraja)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Yi_Karatu
    case 7: __asm__ volatile("br xzr"); break; // Kwara_Daraja/NULL gudanar_Umarni
    }
    return 99;
}
