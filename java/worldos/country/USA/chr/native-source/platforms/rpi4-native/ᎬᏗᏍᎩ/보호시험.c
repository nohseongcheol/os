#include "호출.h"
extern void _start(void);
int ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ) {
    switch (ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kernel_ᏧᎬᏩᎶᏗᏯ ᎪᏪᎶᏗ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ᎪᏪᎶᏗ
    case 2: { // NX stack ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ
        volatile unsigned ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // kernel_ᏧᎬᏩᎶᏗᏯ/NULL ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ
    }
    return 99;
}
