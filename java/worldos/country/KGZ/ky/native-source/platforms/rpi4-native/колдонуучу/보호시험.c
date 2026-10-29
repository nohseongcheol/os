#include "호출.h"
extern void _start(void);
int Баштоо_колдонуучу_програм(int категория_маани) {
    switch (категория_маани) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // өзөк_маани Жазуу
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Жазуу
    case 2: { // NX stack аткаруу_буйрук
        volatile unsigned аткаруу_буйругу_маани = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&аткаруу_буйругу_маани)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Окуу
    case 7: __asm__ volatile("br xzr"); break; // өзөк_маани/NULL аткаруу_буйрук
    }
    return 99;
}
