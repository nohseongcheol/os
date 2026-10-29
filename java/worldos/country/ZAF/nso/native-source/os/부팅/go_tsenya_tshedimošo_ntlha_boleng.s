.code32
.section .multiboot,"a"
.balign 4
.long 0x1badb002
.long 3
.long -(0x1badb002 + 3)

.section .text
.globl _start
_start:
    cli
    cld
    movl %eax, %esi
    movl %ebx, %ebp
    lgdt descriptor_pointer
    ljmp $0x08, $protected_entry
protected_entry:
    movw $0x10, %ax
    movw %ax, %ds
    movw %ax, %es
    movw %ax, %fs
    movw %ax, %gs
    movw %ax, %ss
    movl $bss_start, %edi
    movl $bss_end, %ecx
    subl %edi, %ecx
    xorl %eax, %eax
    rep stosb
    movl %esi, boot_magic
    movl %ebp, boot_info
    movl $stack_top, %esp
    xorl %ebp, %ebp
    # 현재 판은 단일 phethagatša_taelo 흐름의 폴링 커널이다. IRQ를 열지 않는다.
    movb $0xff, %al
    outb %al, $0x21
    outb %al, $0xa1
    call java_entry
    jmp rt_halt

.globl rt_in8, rt_out8, rt_read8, rt_write8
rt_in8:
    movl 4(%esp), %edx
    xorl %eax, %eax
    inb %dx, %al
    ret
rt_out8:
    movl 8(%esp), %edx
    movl 4(%esp), %eax
    outb %al, %dx
    ret
rt_read8:
    movl 4(%esp), %edx
    movzbl (%edx), %eax
    ret
rt_write8:
    movl 8(%esp), %edx
    movl 4(%esp), %eax
    movb %al, (%edx)
    ret

.globl rt_boot_magic, rt_boot_info, rt_pause, rt_halt, rt_test_exit
rt_boot_magic:
    movl boot_magic, %eax
    ret
rt_boot_info:
    movl boot_info, %eax
    ret
rt_pause:
    pause
    ret
rt_halt:
    cli
1:  hlt
    jmp 1b
rt_test_exit:
    movl 4(%esp), %eax
    movw $0xf4, %dx
    outl %eax, %dx
    ret

# boela_sekeng_boemo 가능한 Java 예외 대신 Phošo 번호를 직렬 단말로 알리고 중단한다.
.globl rt_panic
rt_panic:
    movl %eax, %ebp
    movl $panic_text, %esi
1:  lodsb
    testb %al, %al
    jz 2f
    call panic_putchar
    jmp 1b
2:  leal 48(%ebp), %eax
    call panic_putchar
    movb $10, %al
    call panic_putchar
    leal 32(%ebp), %eax
    movw $0xf4, %dx
    outl %eax, %dx
    jmp rt_halt
panic_putchar:
    movb %al, %bl
    movl $100000, %ecx
    movw $0x3fd, %dx
1:  inb %dx, %al
    testb $0x20, %al
    jnz 2f
    loop 1b
    ret
2:  movw $0x3f8, %dx
    movb %bl, %al
    outb %al, %dx
    ret

.section .rodata
.balign 8
.globl descriptor_table
descriptor_table:
    .quad 0
    .quad 0x00cf9a000000ffff
    .quad 0x00cf92000000ffff
    .quad 0x00cffa000000ffff
    .quad 0x00cff2000000ffff
    .quad 0
descriptor_pointer:
    .word 47
    .long descriptor_table
panic_text: .asciz "\nJKOROS PANIC "

.section .bss
.balign 16
boot_magic: .skip 4
boot_info: .skip 4
.balign 16
stack_bottom: .skip 65536
stack_top:
.section .note.GNU-stack,"",@progbits
