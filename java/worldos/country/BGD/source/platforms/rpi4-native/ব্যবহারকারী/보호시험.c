#include "호출.h"
extern void _start(void);
int শুরু_ব্যবহারকারী_অ্যাপ(int বিভাগ_মান) {
    switch (বিভাগ_মান) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // কারনেল_মান লেখা
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text লেখা
    case 2: { // NX stack কার্যকর_করুন_আদেশ
        volatile unsigned নির্দেশ_মান = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&নির্দেশ_মান)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 পড়া
    case 7: __asm__ volatile("br xzr"); break; // কারনেল_মান/NULL কার্যকর_করুন_আদেশ
    }
    return 99;
}
