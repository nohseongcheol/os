#include "ခေါ်လုပ်.h"
extern void _start(void);
int သုံးစွဲသူပရိုဂရမ်စတင်(int 분류) {
    switch (분류) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // အူတိုင်တန်ဖိုး ရေး
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ရေး
    case 2: { // NX stack စက်မောင်း
        volatile unsigned စက်ညွှန်ကြားချက်တန်ဖိုး = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&စက်ညွှန်ကြားချက်တန်ဖိုး)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 ဖတ်
    case 7: __asm__ volatile("br xzr"); break; // အူတိုင်တန်ဖိုး/NULL စက်မောင်း
    }
    return 99;
}
