.text
.globl _start
.type _start, @function
.extern main
.extern _exit
.extern environ
_start:
    xorl %ebp, %ebp
    movl (%esp), %eax
    leal 4(%esp), %ebx
    leal 8(%esp,%eax,4), %ecx
    movl %ecx, environ
    pushl %ecx
    pushl %ebx
    pushl %eax
    call main
    addl $12, %esp
    pushl %eax
    call _exit
1:
    jmp 1b
.size _start, .-_start

.section .note.GNU-stack,"",@progbits
