#include "호출.h"
extern void _start(void);
int დაწყება_მომხმარებელი_აპი(int კატეგორია_მნიშვნელობა) {
    switch (კატეგორია_მნიშვნელობა) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ბირთვი_მნიშვნელობა ჩაწერა
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ჩაწერა
    case 2: { // NX stack შესრულება_ბრძანება
        volatile unsigned ინსტრუქცია_მნიშვნელობა = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ინსტრუქცია_მნიშვნელობა)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 კითხვა
    case 7: __asm__ volatile("br xzr"); break; // ბირთვი_მნიშვნელობა/NULL შესრულება_ბრძანება
    }
    return 99;
}
