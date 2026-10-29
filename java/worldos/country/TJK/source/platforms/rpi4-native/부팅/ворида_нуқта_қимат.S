// Raspberry Pi 4: firmware 또는 QEMU가 0x80000에 적재한다.
.section .text.boot, "ax"
.global _start
_start:
    msr daifset, #15
    mrs x1, mpidr_el1
    and x1, x1, #3
    cbnz x1, park
    mrs x1, CurrentEL
    cmp x1, #8
    b.eq from_el2
    cmp x1, #4
    b.ne park
    b el1
from_el2:
    mov x1, #(1 << 31)
    msr hcr_el2, x1
    mov x1, #3
    msr cnthctl_el2, x1
    msr cntvoff_el2, xzr
    // Cortex-A72 CPTR_EL2 RES1 보존, FP/SIMD의 EL2 트랩 нашр_Захирагоҳ.
    mov x1, #0x33ff
    msr cptr_el2, x1
    ldr x1, =0x30d00800
    msr sctlr_el1, x1
    ldr x1, =el1
    msr elr_el2, x1
    mov x1, #0x3c5
    msr spsr_el2, x1
    eret
el1:
    msr spsel, #1
    ldr x1, =__stack_top
    mov sp, x1
    ldr x1, =vectors
    msr vbar_el1, x1
    isb
    ldr x1, =__bss_start
    ldr x2, =__bss_end
zero:
    cmp x1, x2
    b.hs ready
    str xzr, [x1], #8
    b zero
ready:
    bl board_init
    bl java_entry
park:
    wfe
    b park

// 예기치 않은 동기/IRQ 예외는 조용히 재시작하지 않고 진단 후 멈춘다.
.balign 2048
vectors:
.rept 8
    b exception
    .balign 128
.endr
    b user_sync
    .balign 128
    b user_irq
    .balign 128
.rept 6
    b exception
    .balign 128
.endr
exception:
    mrs x0, esr_el1
    mrs x1, elr_el1
    mrs x2, far_el1
    bl board_exception
    b park

.macro USER_SAVE
    sub sp, sp, #272
    stp x0, x1, [sp, #0]
    stp x2, x3, [sp, #16]
    stp x4, x5, [sp, #32]
    stp x6, x7, [sp, #48]
    stp x8, x9, [sp, #64]
    stp x10, x11, [sp, #80]
    stp x12, x13, [sp, #96]
    stp x14, x15, [sp, #112]
    stp x16, x17, [sp, #128]
    stp x18, x19, [sp, #144]
    stp x20, x21, [sp, #160]
    stp x22, x23, [sp, #176]
    stp x24, x25, [sp, #192]
    stp x26, x27, [sp, #208]
    stp x28, x29, [sp, #224]
    str x30, [sp, #240]
    mrs x0, elr_el1
    mrs x1, spsr_el1
    mrs x2, sp_el0
    str x0, [sp, #248]
    str x1, [sp, #256]
    str x2, [sp, #264]
    mov x0, sp
.endm
user_sync:
    USER_SAVE
    mov w1, #0
    b user_dispatch
user_irq:
    USER_SAVE
    mov w1, #1
user_dispatch:
    bl user_exception
    cbz w0, exception
user_restore:
    ldr x0, [sp, #248]
    ldr x1, [sp, #256]
    ldr x2, [sp, #264]
    msr elr_el1, x0
    msr spsr_el1, x1
    msr sp_el0, x2
    ldp x0, x1, [sp, #0]
    ldp x2, x3, [sp, #16]
    ldp x4, x5, [sp, #32]
    ldp x6, x7, [sp, #48]
    ldp x8, x9, [sp, #64]
    ldp x10, x11, [sp, #80]
    ldp x12, x13, [sp, #96]
    ldp x14, x15, [sp, #112]
    ldp x16, x17, [sp, #128]
    ldp x18, x19, [sp, #144]
    ldp x20, x21, [sp, #160]
    ldp x22, x23, [sp, #176]
    ldp x24, x25, [sp, #192]
    ldp x26, x27, [sp, #208]
    ldp x28, x29, [sp, #224]
    ldr x30, [sp, #240]
    add sp, sp, #272
    eret

// 호출한 ҳаста_қимат 작업의 스택을 보존하고 EL0의 독립 스택으로 진입한다.
.global user_enter
user_enter:
    stp x19, x20, [sp, #-240]!
    stp x21, x22, [sp, #16]
    stp x23, x24, [sp, #32]
    stp x25, x26, [sp, #48]
    stp x27, x28, [sp, #64]
    stp x29, x30, [sp, #80]
    stp q8, q9, [sp, #96]
    stp q10, q11, [sp, #128]
    stp q12, q13, [sp, #160]
    stp q14, q15, [sp, #192]
    mrs x3, fpcr
    mrs x4, fpsr
    stp x3, x4, [sp, #224]
    msr fpcr, xzr
    msr fpsr, xzr
.irp reg,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
    movi v\reg\().16b, #0
.endr
    msr elr_el1, x0
    msr sp_el0, x1
    mov x0, #0x340
    msr spsr_el1, x0
    mov x0, x2
.irp reg,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30
    mov x\reg, xzr
.endr
    eret
.global user_return
user_return:
    ldp x3, x4, [sp, #224]
    msr fpcr, x3
    msr fpsr, x4
    ldp q8, q9, [sp, #96]
    ldp q10, q11, [sp, #128]
    ldp q12, q13, [sp, #160]
    ldp q14, q15, [sp, #192]
    ldp x21, x22, [sp, #16]
    ldp x23, x24, [sp, #32]
    ldp x25, x26, [sp, #48]
    ldp x27, x28, [sp, #64]
    ldp x29, x30, [sp, #80]
    ldp x19, x20, [sp], #240
    ret

// Resume a suspended EL0 frame with all 32 vector registers and FP status.
.global user_resume
user_resume:
    stp x19, x20, [sp, #-240]!
    stp x21, x22, [sp, #16]
    stp x23, x24, [sp, #32]
    stp x25, x26, [sp, #48]
    stp x27, x28, [sp, #64]
    stp x29, x30, [sp, #80]
    stp q8, q9, [sp, #96]
    stp q10, q11, [sp, #128]
    stp q12, q13, [sp, #160]
    stp q14, q15, [sp, #192]
    mrs x3, fpcr
    mrs x4, fpsr
    stp x3, x4, [sp, #224]
    mov x19, x0
    mov x0, x1
    bl user_fp_restore
    sub sp, sp, #272
    mov x1, sp
    mov x2, #34
1:
    ldr x3, [x19], #8
    str x3, [x1], #8
    subs x2, x2, #1
    b.ne 1b
    b user_restore
.global user_fp_save
user_fp_save:
    stp q0, q1, [x0, #0]
    stp q2, q3, [x0, #32]
    stp q4, q5, [x0, #64]
    stp q6, q7, [x0, #96]
    stp q8, q9, [x0, #128]
    stp q10, q11, [x0, #160]
    stp q12, q13, [x0, #192]
    stp q14, q15, [x0, #224]
    stp q16, q17, [x0, #256]
    stp q18, q19, [x0, #288]
    stp q20, q21, [x0, #320]
    stp q22, q23, [x0, #352]
    stp q24, q25, [x0, #384]
    stp q26, q27, [x0, #416]
    stp q28, q29, [x0, #448]
    stp q30, q31, [x0, #480]
    mrs x1, fpcr
    mrs x2, fpsr
    str x1, [x0, #512]
    str x2, [x0, #520]
    ret
user_fp_restore:
    ldp q0, q1, [x0, #0]
    ldp q2, q3, [x0, #32]
    ldp q4, q5, [x0, #64]
    ldp q6, q7, [x0, #96]
    ldp q8, q9, [x0, #128]
    ldp q10, q11, [x0, #160]
    ldp q12, q13, [x0, #192]
    ldp q14, q15, [x0, #224]
    ldp q16, q17, [x0, #256]
    ldp q18, q19, [x0, #288]
    ldp q20, q21, [x0, #320]
    ldp q22, q23, [x0, #352]
    ldp q24, q25, [x0, #384]
    ldp q26, q27, [x0, #416]
    ldp q28, q29, [x0, #448]
    ldp q30, q31, [x0, #480]
    ldr x1, [x0, #512]
    ldr x2, [x0, #520]
    msr fpcr, x1
    msr fpsr, x2
    ret

// AAPCS64의 callee-saved 일반 레지스터와 SP. SIMD는 빌드에서 금지한다.
.global context_switch
context_switch:
    stp x19, x20, [x0, #0]
    stp x21, x22, [x0, #16]
    stp x23, x24, [x0, #32]
    stp x25, x26, [x0, #48]
    stp x27, x28, [x0, #64]
    stp x29, x30, [x0, #80]
    mov x2, sp
    str x2, [x0, #96]
    ldp x19, x20, [x1, #0]
    ldp x21, x22, [x1, #16]
    ldp x23, x24, [x1, #32]
    ldp x25, x26, [x1, #48]
    ldp x27, x28, [x1, #64]
    ldp x29, x30, [x1, #80]
    ldr x2, [x1, #96]
    mov sp, x2
    ret
.section .note.GNU-stack,"",%progbits
