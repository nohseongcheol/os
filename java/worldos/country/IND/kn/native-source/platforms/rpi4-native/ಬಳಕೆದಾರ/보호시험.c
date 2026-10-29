#include "호출.h"
extern void _start(void);
int ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(int ವರ್ಗ_ಮೌಲ್ಯ) {
    switch (ವರ್ಗ_ಮೌಲ್ಯ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ಕರ್ನಲ್_ಮೌಲ್ಯ ಬರೆ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ಬರೆ
    case 2: { // NX stack ಪೂರೈಸು_ಆದೇಶ
        volatile unsigned ಸೂಚನೆ_ಮೌಲ್ಯ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ಸೂಚನೆ_ಮೌಲ್ಯ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 ಓದು
    case 7: __asm__ volatile("br xzr"); break; // ಕರ್ನಲ್_ಮೌಲ್ಯ/NULL ಪೂರೈಸು_ಆದೇಶ
    }
    return 99;
}
