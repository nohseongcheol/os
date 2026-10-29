#include "호출.h"
extern void _start(void);
int شروع_کاربر_برنامه(int دسته_مقدار) {
    switch (دسته_مقدار) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // هسته_مقدار نوشتن
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text نوشتن
    case 2: { // NX stack اجرا_فرمان
        volatile unsigned دستورالعمل_مقدار = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&دستورالعمل_مقدار)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 خواندن
    case 7: __asm__ volatile("br xzr"); break; // هسته_مقدار/NULL اجرا_فرمان
    }
    return 99;
}
