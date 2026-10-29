.code32
.text
.globl _start
_start:
    cld
    andl $-16, %esp
    call jkoros_main
    subl $12, %esp
    pushl %eax
    call _exit
.section .note.GNU-stack,"",@progbits
