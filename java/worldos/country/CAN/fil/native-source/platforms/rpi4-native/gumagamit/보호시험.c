#include "호출.h"
extern void _start(void);
int Start_gumagamit_app(int kategorya_VALUE) {
    switch (kategorya_VALUE) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kernel_VALUE sumulat
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text sumulat
    case 2: { // NX stack Mag_execute_utos
        volatile unsigned instruksiyon_VALUE = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&instruksiyon_VALUE)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // kernel_VALUE/NULL Mag_execute_utos
    }
    return 99;
}
