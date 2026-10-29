#include "호출.h"
extern void _start(void);
int Start_kaiwhakamahi_kaupapa(int kāwai_uara) {
    switch (kāwai_uara) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kākano_uara_0611a8a8 Tuhia
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Tuhia
    case 2: { // NX stack kawe_tono
        volatile unsigned tohutohu_uara = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&tohutohu_uara)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Pānuitia
    case 7: __asm__ volatile("br xzr"); break; // kākano_uara_0611a8a8/NULL kawe_tono
    }
    return 99;
}
