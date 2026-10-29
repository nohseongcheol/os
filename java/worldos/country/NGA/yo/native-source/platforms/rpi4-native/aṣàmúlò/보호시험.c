#include "호출.h"
extern void _start(void);
int bẹ̀rẹ̀_aṣàmúlò_àtòjọ_ètò(int ìsọ̀rí_iye) {
    switch (ìsọ̀rí_iye) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kánẹ́ẹ̀lì_iye Kọ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Kọ
    case 2: { // NX stack ṣiṣẹ́_àṣẹ
        volatile unsigned ìtọ́sọ́nà_iye = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ìtọ́sọ́nà_iye)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Kàá
    case 7: __asm__ volatile("br xzr"); break; // kánẹ́ẹ̀lì_iye/NULL ṣiṣẹ́_àṣẹ
    }
    return 99;
}
