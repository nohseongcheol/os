#include "호출.h"
extern void _start(void);
int qala_umsebenzisi_inkqubo(int udidi_ixabiso) {
    switch (udidi_ixabiso) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ikheneli_ixabiso Bhala
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Bhala
    case 2: { // NX stack ukwenza_umyalelo
        volatile unsigned umyalelo_ixabiso = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&umyalelo_ixabiso)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Funda
    case 7: __asm__ volatile("br xzr"); break; // ikheneli_ixabiso/NULL ukwenza_umyalelo
    }
    return 99;
}
