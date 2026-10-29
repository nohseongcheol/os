#include "호출.h"
extern void _start(void);
int huɓɓude_kuutoro_tafirde(int kategorii_njaru) {
    switch (kategorii_njaru) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // aaluude_njaru winndude
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text winndude
    case 2: { // NX stack 실행
        volatile unsigned yamiroore_njaru = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&yamiroore_njaru)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // aaluude_njaru/NULL 실행
    }
    return 99;
}
