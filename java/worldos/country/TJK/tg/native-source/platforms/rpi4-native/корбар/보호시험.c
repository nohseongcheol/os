#include "호출.h"
extern void _start(void);
int Оғоз_корбар_барнома(int категория_қимат) {
    switch (категория_қимат) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ҳаста_қимат Навиштан
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Навиштан
    case 2: { // NX stack иҷро_кардан_фармон
        volatile unsigned дастур_қимат = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&дастур_қимат)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Хондан
    case 7: __asm__ volatile("br xzr"); break; // ҳаста_қимат/NULL иҷро_кардан_фармон
    }
    return 99;
}
