#include "호출.h"
extern void _start(void);
int เริ่ม_ผู้ใช้_แอป(int ประเภท_ค่า) {
    switch (ประเภท_ค่า) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // เคอร์เนล_ค่า เขียน
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text เขียน
    case 2: { // NX stack ดําเนินการ_คําสั่ง
        volatile unsigned 명령어 = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&명령어)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 อ่าน
    case 7: __asm__ volatile("br xzr"); break; // เคอร์เนล_ค่า/NULL ดําเนินการ_คําสั่ง
    }
    return 99;
}
