#include "आवाहन.h"
extern void _start(void);
int प्रारंभ_प्रयोक्ता_अनुप्रयोग(int वर्गवारी_मूल्य) {
    switch (वर्गवारी_मूल्य) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // गाभा_मूल्य लेखन
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text लेखन
    case 2: { // NX stack आज्ञा_कार्यवाही_करा
        volatile unsigned निर्देश_मूल्य = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&निर्देश_मूल्य)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 वाचन
    case 7: __asm__ volatile("br xzr"); break; // गाभा_मूल्य/NULL आज्ञा_कार्यवाही_करा
    }
    return 99;
}
