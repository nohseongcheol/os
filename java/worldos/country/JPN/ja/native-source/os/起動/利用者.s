.code32
.text
.globl rt_user_setup, rt_enter_user, rt_user_clear, rt_millis
.globl rt_in32, rt_out32, rt_out16, rt_app_blob, rt_app_blob_size, rt_net_memory
rt_in32:
    movl 4(%esp), %edx
    inl %dx, %eax
    ret
.globl rt_in16
rt_in16:
    movl 4(%esp), %edx
    xorl %eax, %eax
    inw %dx, %ax
    ret
rt_out32:
    movl 8(%esp), %edx
    movl 4(%esp), %eax
    outl %eax, %dx
    ret
rt_out16:
    movl 8(%esp), %edx
    movl 4(%esp), %eax
    outw %ax, %dx
    ret
rt_app_blob:
    movl $app_blob_start, %eax
    ret
rt_app_blob_size:
    movl $app_blob_end, %eax
    subl $app_blob_start, %eax
    ret
rt_net_memory:
    movl $network_dma, %eax
    ret
.globl rt_file_memory
rt_file_memory:
    movl $ram_files, %eax
    ret
.globl rt_file_bundle, rt_file_bundle_size
rt_file_bundle:
    movl $java_files, %eax
    ret
rt_file_bundle_size:
    movl $java_files_end-java_files, %eax
    ret
rt_millis:
    imull $10, ticks, %eax
    ret
.globl rt_user_remaining
rt_user_remaining:
    movl user_deadline, %eax
    subl ticks, %eax
    imull $10, %eax
    ret

rt_user_setup:
    cli
    # TSS의 SS0/ESP0 및 I/O bitmap 境界位置上限: ring 3의 모든 機器ポート アクセス入口 禁止対象値.
    movl $interrupt_stack_top, task_state+4
    movl $0x10, task_state+8
    movw $104, task_state+102
    movl $task_state, %eax
    movw $103, descriptor_table+40
    movw %ax, descriptor_table+42
    shrl $16, %eax
    movb %al, descriptor_table+44
    movb $0x89, descriptor_table+45
    movb $0, descriptor_table+46
    movb %ah, descriptor_table+47
    movw $0x28, %ax
    ltr %ax
    # 0..16MiB: supervisor identity. 64..68MiB: private user region at physical 8MiB.
    movl $0x00000083, page_directory
    movl $0x00400083, page_directory+4
    movl $0x00800083, page_directory+8
    movl $0x00c00083, page_directory+12
    movl $0x00800087, page_directory+64
    movl %cr4, %eax
    orl $0x10, %eax
    movl %eax, %cr4
    movl $page_directory, %eax
    movl %eax, %cr3
    movl %cr0, %eax
    orl $0x80010000, %eax
    movl %eax, %cr0
    # 모든 CPU 예외와 syscall gate. 剰余値 인터럽트는 마스크한다.
    xorl %ecx, %ecx
1:  movl exception_addresses(,%ecx,4), %eax
    movl $0x8e, %edx
    call set_gate
    incl %ecx
    cmpl $32, %ecx
    jne 1b
    movl $32, %ecx
    movl $timer_interrupt, %eax
    movl $0x8e, %edx
    call set_gate
    movl $128, %ecx
    movl $system_call, %eax
    movl $0xee, %edx
    call set_gate
    lidt interrupt_pointer
    movb $0x11, %al
    outb %al, $0x20
    outb %al, $0xa0
    movb $0x20, %al
    outb %al, $0x21
    movb $0x28, %al
    outb %al, $0xa1
    movb $4, %al
    outb %al, $0x21
    movb $2, %al
    outb %al, $0xa1
    movb $1, %al
    outb %al, $0x21
    outb %al, $0xa1
    movb $0xfe, %al
    outb %al, $0x21
    movb $0xff, %al
    outb %al, $0xa1
    # PIT 100Hz. 네트워크 대기와 利用者 プログラム 3초 命令実行 상한에 사용한다.
    movb $0x36, %al
    outb %al, $0x43
    movb $0x9c, %al
    outb %al, $0x40
    movb $0x2e, %al
    outb %al, $0x40
    sti
    ret
set_gate:
    movw %ax, interrupt_table(,%ecx,8)
    movw $8, interrupt_table+2(,%ecx,8)
    movb $0, interrupt_table+4(,%ecx,8)
    movb %dl, interrupt_table+5(,%ecx,8)
    shrl $16, %eax
    movw %ax, interrupt_table+6(,%ecx,8)
    ret

rt_user_clear:
    cld
    movl $0x00800000, %edi
    movl $1048576, %ecx
    xorl %eax, %eax
    rep stosl
    ret
rt_enter_user:
    cli
    pushl %ebp
    movl %esp, kernel_resume_stack
    movl 12(%esp), %ecx
    movl 8(%esp), %edx
    movl $1, user_active
    movl ticks, %eax
    addl $300, %eax
    movl %eax, user_deadline
    movw $0x23, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %fs
    movw %ax, %gs
    pushl $0x23
    pushl %edx
    pushl $0x202
    pushl $0x1b
    pushl %ecx
    iret
user_leave:
    cli
    movw $0x10, %dx
    movw %dx, %ds
    movw %dx, %es
    movw %dx, %fs
    movw %dx, %gs
    movl kernel_resume_stack, %esp
    popl %ebp
    movl $0, user_active
    sti
    ret

system_call:
    cld
    pushal
    pushl %ds
    pushl %es
    movw $0x10, %ax
    movw %ax, %ds
    movw %ax, %es
    movl %esp, %ebp
    cmpl $0, 36(%ebp)
    je system_exit
    movl ticks, %eax
    subl user_deadline, %eax
    js 1f
    movl $124, %eax
    jmp user_leave
1:
    # 中核値 syscall은 bounded polling 중 PIT를 허용한다.
    sti
    pushl 36(%ebp)
    pushl 24(%ebp)
    pushl 32(%ebp)
    pushl 28(%ebp)
    pushl 12(%ebp)
    pushl 8(%ebp)
    call kernel_dispatch
    addl $24, %esp
    cli
    movl %eax, 36(%ebp)
    movl ticks, %eax
    subl user_deadline, %eax
    js 1f
    movl $124, %eax
    jmp user_leave
1:
    popl %es
    popl %ds
    popal
    iret
system_exit:
    movl 24(%ebp), %eax
    jmp user_leave

timer_interrupt:
    cld
    pushal
    pushl %ds
    movw $0x10, %ax
    movw %ax, %ds
    incl ticks
    movb $0x20, %al
    outb %al, $0x20
    cmpl $0, user_active
    je 1f
    testb $3, 40(%esp)
    jz 1f
    movl ticks, %eax
    subl user_deadline, %eax
    js 1f
    movl $124, %eax
    jmp user_leave
1:  popl %ds
    popal
    iret

.macro EXCEPTION number, error=0
exception_\number:
.if !\error
    pushl $0
.endif
    pushl $\number
    jmp exception_common
.endm
.irp n,0,1,2,3,4,5,6,7,9,15,16,18,19,20,22,23,24,25,26,27,28,31
EXCEPTION \n
.endr
.irp n,8,10,11,12,13,14,17,21,29,30
EXCEPTION \n,1
.endr
exception_common:
    cld
    movw $0x10, %ax
    movw %ax, %ds
    movw %ax, %es
    testb $3, 12(%esp)
    jz kernel_exception
    movl (%esp), %eax
    addl $128, %eax
    jmp user_leave
kernel_exception:
    movl (%esp), %eax
    jmp rt_panic

.section .rodata
.balign 16
java_files:
.incbin "build/java-files.bin"
java_files_end:
exception_addresses:
.irp n,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
    .long exception_\n
.endr
interrupt_pointer:
    .word 2047
    .long interrupt_table
.section .bss
.balign 4096
page_directory: .skip 4096
.balign 16
interrupt_table: .skip 2048
task_state: .skip 104
ticks: .skip 4
user_active: .skip 4
user_deadline: .skip 4
kernel_resume_stack: .skip 4
.balign 16
interrupt_stack: .skip 65536
interrupt_stack_top:
.balign 256
network_dma: .skip 16384
.balign 4096
ram_files: .skip 131072
.section .note.GNU-stack,"",@progbits
