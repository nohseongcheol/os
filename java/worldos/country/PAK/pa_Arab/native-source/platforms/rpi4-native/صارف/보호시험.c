#include "호출.h"
extern void _start(void);
int مکھ_صارف_ایپ(int زمرہ_قدر) {
    switch (زمرہ_قدر) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // کرنل_قدر لکھو
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text لکھو
    case 2: { // NX stack نفاذ_کرو_حکم
        volatile unsigned ہدایت_قدر = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ہدایت_قدر)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // کرنل_قدر/NULL نفاذ_کرو_حکم
    }
    return 99;
}
