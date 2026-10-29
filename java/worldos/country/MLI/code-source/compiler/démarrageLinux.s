.code32
.text
.globl _start
_start:
    cld
    call java_entry
    movl %eax, %ebx
    movl $1, %eax
    int $0x80
.globl rt_panic
rt_panic:
    leal 100(%eax), %ebx
    movl $1, %eax
    int $0x80
.section .note.GNU-stack,"",@progbits
