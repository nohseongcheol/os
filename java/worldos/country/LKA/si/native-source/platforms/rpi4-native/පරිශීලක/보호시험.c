#include "호출.h"
extern void _start(void);
int ඇරඹුම_පරිශීලක_යෙදු(int ප්_රවර්ගය_අගය) {
    switch (ප්_රවර්ගය_අගය) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // කර්නලය_අගය ලිවීම
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ලිවීම
    case 2: { // NX stack ක්_රියාත්මක_කරන්න_විධානය
        volatile unsigned උපදෙස_අගය = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&උපදෙස_අගය)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 කියවීම
    case 7: __asm__ volatile("br xzr"); break; // කර්නලය_අගය/NULL ක්_රියාත්මක_කරන්න_විධානය
    }
    return 99;
}
