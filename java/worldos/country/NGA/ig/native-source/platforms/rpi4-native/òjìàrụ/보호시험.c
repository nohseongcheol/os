#include "호출.h"
extern void _start(void);
int Mbido_òjìàrụ_app(int otu_valuu_4b6d6445) {
    switch (otu_valuu_4b6d6445) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // mkpụrụobī_kọmpùta_valuu Chekwaa_ozi
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Chekwaa_ozi
    case 2: { // NX stack mee_nnyemiwu
        volatile unsigned okwunkụzi_valuu = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&okwunkụzi_valuu)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Wepụta_ọzi
    case 7: __asm__ volatile("br xzr"); break; // mkpụrụobī_kọmpùta_valuu/NULL mee_nnyemiwu
    }
    return 99;
}
