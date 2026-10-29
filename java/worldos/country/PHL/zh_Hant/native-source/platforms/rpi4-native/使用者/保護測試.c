#include "調用.h"
extern void _start(void);
int 開始用戶程式(int 分類值) {
    switch (分類值) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // 內核值 寫入
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text 寫入
    case 2: { // NX stack 執行命令
        volatile unsigned 指令值 = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&指令值)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 讀取
    case 7: __asm__ volatile("br xzr"); break; // 內核值/NULL 執行命令
    }
    return 99;
}
