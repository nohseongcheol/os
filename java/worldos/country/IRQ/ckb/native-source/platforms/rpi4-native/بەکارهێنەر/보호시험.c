#include "호출.h"
extern void _start(void);
int دەستپێك_بەکارهێنەر_بەرنامە(int پۆل_نرخ) {
    switch (پۆل_نرخ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // کوورەک_نرخ ڕایت_کردن
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ڕایت_کردن
    case 2: { // NX stack جێبەجێکردن_فەرمان
        volatile unsigned ڕێنمایی_نرخ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ڕێنمایی_نرخ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // کوورەک_نرخ/NULL جێبەجێکردن_فەرمان
    }
    return 99;
}
