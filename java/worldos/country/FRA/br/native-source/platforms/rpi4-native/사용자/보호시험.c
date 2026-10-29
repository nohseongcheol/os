#include "호출.h"
extern void _start(void);
int 사용자시작(int 분류) {
    switch (분류) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // 커널 Skrivañ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Skrivañ
    case 2: { // NX stack 실행
        volatile unsigned 명령어 = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&명령어)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Lenn
    case 7: __asm__ volatile("br xzr"); break; // 커널/NULL 실행
    }
    return 99;
}
