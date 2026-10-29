#include "호출.h"
extern void _start(void);
int بدء_مستخدم_تطبيق(int فئة_قيمة) {
    switch (فئة_قيمة) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // نواة_قيمة كتابة
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text كتابة
    case 2: { // NX stack ينفذ_أمر
        volatile unsigned تعليمة_قيمة = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&تعليمة_قيمة)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 قراءة
    case 7: __asm__ volatile("br xzr"); break; // نواة_قيمة/NULL ينفذ_أمر
    }
    return 99;
}
