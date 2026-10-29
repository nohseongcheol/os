.section .text.start,"ax"
.global _start
_start:
    bl user_start
    mov x8, #6
    svc #0
1:  b 1b
.section .note.jkoros,"a",%note
.balign 4
.long 7, 4, 1
.asciz "JKOROS"
.balign 4
.long 1
.section .note.GNU-stack,"",%progbits
