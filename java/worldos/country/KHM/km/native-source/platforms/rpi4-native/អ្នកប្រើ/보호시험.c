#include "호출.h"
extern void _start(void);
int ផ្តើម_អ្នកប្រើ_កម្មវិធី(int ប្រភេទ_តំលៃ) {
    switch (ប្រភេទ_តំលៃ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ខឺណេល_តំលៃ សរសេរ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text សរសេរ
    case 2: { // NX stack អនុវត្ត_ពាក្យបញ្ជា
        volatile unsigned ការណែនាំ_តំលៃ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ការណែនាំ_តំលៃ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 អាន
    case 7: __asm__ volatile("br xzr"); break; // ខឺណេល_តំលៃ/NULL អនុវត្ត_ពាក្យបញ្ជា
    }
    return 99;
}
