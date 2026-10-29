#include "호출.h"
extern void _start(void);
int Door_kiy_jariñoo_internet_jëfekaay(int ngiir_xëyma) {
    switch (ngiir_xëyma) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // xoox_xëyma biir
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text biir
    case 2: { // NX stack def_ndigel
        volatile unsigned ndigal_xëyma = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ndigal_xëyma)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // xoox_xëyma/NULL def_ndigel
    }
    return 99;
}
