#include "호출.h"
extern void _start(void);
int પ્રારંભ_ઉપયોગકર્તા_એપ્લિકેશન(int શ્રેણી_મૂલ્ય) {
    switch (શ્રેણી_મૂલ્ય) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // કર્નેલ_મૂલ્ય લખો
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text લખો
    case 2: { // NX stack અમલ_કરો_આદેશ
        volatile unsigned સૂચના_મૂલ્ય = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&સૂચના_મૂલ્ય)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 વાંચો
    case 7: __asm__ volatile("br xzr"); break; // કર્નેલ_મૂલ્ય/NULL અમલ_કરો_આદેશ
    }
    return 99;
}
