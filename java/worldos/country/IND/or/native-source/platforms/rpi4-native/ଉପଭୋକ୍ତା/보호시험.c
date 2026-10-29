#include "호출.h"
extern void _start(void);
int ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(int ବର୍ଗ_ମୂଲ୍ୟ) {
    switch (ବର୍ଗ_ମୂଲ୍ୟ) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ ଲେଖନ୍ତୁ
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text ଲେଖନ୍ତୁ
    case 2: { // NX stack ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ
        volatile unsigned ପରାମର୍ଶ_ମୂଲ୍ୟ = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&ପରାମର୍ଶ_ମୂଲ୍ୟ)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 ପଢନ୍ତୁ
    case 7: __asm__ volatile("br xzr"); break; // କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ/NULL ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ
    }
    return 99;
}
