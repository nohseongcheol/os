#include "호출.h"
extern void _start(void);
int ప్రారంభం_వినియోగదారు_అనువర్తనం(int వర్గం_మూల్యం) {
    switch (వర్గం_మూల్యం) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // కెర్నల్_మూల్యం వ్రాయుము
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text వ్రాయుము
    case 2: { // NX stack అమలు_చేయి_ఆదేశం
        volatile unsigned సూచన_మూల్యం = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&సూచన_మూల్యం)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 చదువు
    case 7: __asm__ volatile("br xzr"); break; // కెర్నల్_మూల్యం/NULL అమలు_చేయి_ఆదేశం
    }
    return 99;
}
