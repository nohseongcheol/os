#include "호출.h"
extern void _start(void);
int ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ(int ຫມວດ_ຄ່າ) {
    switch (ຫມວດ_ຄ່າ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // ແກນກາງ_ຄ່າ ຂຽນ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ຂຽນ
    case 2: { // NX stack ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ
        volatile unsigned ຄໍາແນະນໍາ_ຄ່າ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ຄໍາແນະນໍາ_ຄ່າ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 읽기
    case 7: __asm__ volatile("br xzr"); break; // ແກນກາງ_ຄ່າ/NULL ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ
    }
    return 99;
}
