#include "호출.h"
extern void _start(void);
int আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্(int বর্গ_মান) {
    switch (বর্গ_মান) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // কাৰ্ণেল_মান লিখা
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text লিখা
    case 2: { // NX stack নিষ্পাদন_আদেশ
        volatile unsigned নিৰ্দেশনা_মান = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&নিৰ্দেশনা_মান)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 পড়া
    case 7: __asm__ volatile("br xzr"); break; // কাৰ্ণেল_মান/NULL নিষ্পাদন_আদেশ
    }
    return 99;
}
