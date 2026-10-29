#include "호출.h"
extern void _start(void);
int HASI_erabiltzaile_aplik(int Kategoria_balio) {
    switch (Kategoria_balio) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // nukleo_balio Idatzi
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Idatzi
    case 2: { // NX stack exekutatu_komando
        volatile unsigned instrukzio_balio_4c26ea1b = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&instrukzio_balio_4c26ea1b)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Irakurri
    case 7: __asm__ volatile("br xzr"); break; // nukleo_balio/NULL exekutatu_komando
    }
    return 99;
}
