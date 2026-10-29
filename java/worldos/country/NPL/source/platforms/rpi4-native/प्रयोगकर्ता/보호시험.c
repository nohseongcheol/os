#include "호출.h"
extern void _start(void);
int सुरु_प्रयोगकर्ता_अनुप्रयोग(int कोटि_मान) {
    switch (कोटि_मान) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // कर्णेल_मान लेख्नुहोस्
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text लेख्नुहोस्
    case 2: { // NX stack कार्यान्वयन_गर्नुहोस्_आदेश
        volatile unsigned निर्देशन_मान = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&निर्देशन_मान)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 पढनुहोस्
    case 7: __asm__ volatile("br xzr"); break; // कर्णेल_मान/NULL कार्यान्वयन_गर्नुहोस्_आदेश
    }
    return 99;
}
