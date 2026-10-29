#include "호출.h"
extern void _start(void);
int START_usuario_apl(int Categoría_VALOR) {
    switch (Categoría_VALOR) {
    case 0: *(volatile unsigned *)0x80000 = 1; break; // kernel_VALOR Escritura
    case 1: *(volatile unsigned *)(uintptr_t)_start = 0; break; // RX text Escritura
    case 2: { // NX stack executar_comando
        volatile unsigned instrución_VALOR_4c26ea1b = 0xd65f03c0; // ret
        ((void (*)(void))(uintptr_t)&instrución_VALOR_4c26ea1b)(); break;
    }
    case 3: return *(volatile unsigned *)0x02eff000; // stack guard
    case 4: __asm__ volatile("msr sctlr_el1, xzr"); break;
    case 5: for (;;) __asm__ volatile("nop"); // SVC 없는 무한 반복도 IRQ로 회수
    case 6: return *(volatile unsigned *)0xfe201000; // MMIO 직접 Lectura
    case 7: __asm__ volatile("br xzr"); break; // kernel_VALOR/NULL executar_comando
    }
    return 99;
}
