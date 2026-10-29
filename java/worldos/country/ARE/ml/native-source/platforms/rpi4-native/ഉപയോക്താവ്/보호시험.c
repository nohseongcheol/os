#include "호출.h"
extern void _start(void);
int ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം(int വകുപ്പ്_മൂല്യം) {
    switch (വകുപ്പ്_മൂല്യം) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // കെര്_ണല്_മൂല്യം എഴുത്തു്
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text എഴുത്തു്
    case 2: { // NX stack നടപ്പാക്കുക_കമാന്_ഡ്
        volatile unsigned നിര്_ദേശം_മൂല്യം = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&നിര്_ദേശം_മൂല്യം)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 വായന
    case 7: __asm__ volatile("br xzr"); break; // കെര്_ണല്_മൂല്യം/NULL നടപ്പാക്കുക_കമാന്_ഡ്
    }
    return 99;
}
