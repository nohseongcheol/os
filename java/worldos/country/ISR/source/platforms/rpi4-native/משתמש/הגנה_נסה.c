#include "호출.h"
extern void _start(void);
int התחל_משתמש_תוכנית(int אזור_ערך) {
    switch (אזור_ערך) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ליבה_ערך כתוב
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text כתוב
    case 2: { // NX stack לבצע_פקודה
        volatile unsigned הוראה_ערך = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&הוראה_ערך)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 קרא
    case 7: __asm__ volatile("br xzr"); break; // ליבה_ערך/NULL לבצע_פקודה
    }
    return 99;
}
