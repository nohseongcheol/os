#include "호출.h"
extern void _start(void);
int Старт_корисник_програм(int област_вриједност) {
    switch (област_вриједност) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // језгро_вриједност Пише
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Пише
    case 2: { // NX stack Изврши_команда
        volatile unsigned програмска_наредба_вриједност = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&програмска_наредба_вриједност)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Чита
    case 7: __asm__ volatile("br xzr"); break; // језгро_вриједност/NULL Изврши_команда
    }
    return 99;
}
