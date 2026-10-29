#include "호출.h"
extern void _start(void);
int प्रारंभ_उपयोगकर्ता_ऐप(int श्रेणी_मान) {
    switch (श्रेणी_मान) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // कर्नेल_मान लिखें
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text लिखें
    case 2: { // NX stack निष्पादित_करें_आदेश
        volatile unsigned 명령어 = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&명령어)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 पढ़ें
    case 7: __asm__ volatile("br xzr"); break; // कर्नेल_मान/NULL निष्पादित_करें_आदेश
    }
    return 99;
}
