#include "호출.h"
extern void _start(void);
int Start_उपेगकर्तो_एप्लिकेशन(int वर्ग_मोल) {
    switch (वर्ग_मोल) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // कर्नेल_मोल बरोवचें
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text बरोवचें
    case 2: { // NX stack पाळो_दिवचो_आदेश
        volatile unsigned समजावणी_मोल = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&समजावणी_मोल)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // कर्नेल_मोल/NULL पाळो_दिवचो_आदेश
    }
    return 99;
}
