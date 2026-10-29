#include "呼出.h"
extern void _start(void);
int 利用者プログラム開始処理(int 分類値) {
    switch (分類値) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // 中核値 書込
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text 書込
    case 2: { // NX stack 命令実行
        volatile unsigned 命令語値 = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&命令語値)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 読取
    case 7: __asm__ volatile("br xzr"); break; // 中核値/NULL 命令実行
    }
    return 99;
}
