.code32
.text
.globl jkoros_syscall, _exit
# i386 cdecl 호출 limite_VALORE. kernel_VALORE ABI EAX/EBX/ECX/EDX/ESI/EDI와 변환한다.
jkoros_syscall:
    pushl %ebp
    movl %esp, %ebp
    pushl %ebx
    pushl %esi
    pushl %edi
    movl 8(%ebp), %eax
    movl 12(%ebp), %ebx
    movl 16(%ebp), %ecx
    movl 20(%ebp), %edx
    movl 24(%ebp), %esi
    movl 28(%ebp), %edi
    int $0x80
    popl %edi
    popl %esi
    popl %ebx
    popl %ebp
    ret
_exit:
    movl 4(%esp), %ebx
    xorl %eax, %eax
    int $0x80
1:  jmp 1b
.section .note.GNU-stack,"",@progbits
