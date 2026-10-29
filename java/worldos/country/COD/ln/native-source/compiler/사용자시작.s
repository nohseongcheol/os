.code32
.text
.globl _start, rt_panic
_start:
    cld
    call java_entry
    movl %eax, %ebx
    xorl %eax, %eax
    int $0x80
1:  jmp 1b
rt_panic:
    leal 100(%eax), %ebx
    xorl %eax, %eax
    int $0x80
1:  jmp 1b

.macro ONE name, number
.globl \name
\name:
    movl 4(%esp), %ebx
    movl $\number, %eax
    int $0x80
    ret
.endm
ONE us_write, 1
ONE us_argv, 3
ONE us_open, 10
ONE us_close, 13
ONE us_peer_address, 15
ONE us_peer_port, 16
ONE us_putchar, 22
ONE us_fd_close, 33
ONE us_fd_sync, 47
.globl us_argc, us_address, us_privilege, us_send, us_recv
us_argc:
    movl $2, %eax
    int $0x80
    ret
us_address:
    movl $14, %eax
    int $0x80
    ret
us_privilege:
    xorl %eax, %eax
    movw %cs, %ax
    andl $3, %eax
    ret
us_send:
    movl 20(%esp), %ebx
    movl 16(%esp), %ecx
    movl 12(%esp), %edx
    movl 8(%esp), %esi
    movl 4(%esp), %edi
    movl $11, %eax
    int $0x80
    ret
us_recv:
    movl 12(%esp), %ebx
    movl 8(%esp), %ecx
    movl 4(%esp), %edx
    movl $12, %eax
    int $0x80
    ret
.globl us_file_read, us_file_write
us_file_read:
    movl 8(%esp), %ebx
    movl 4(%esp), %ecx
    movl $20, %eax
    int $0x80
    ret
us_file_write:
    movl 12(%esp), %ebx
    movl 8(%esp), %ecx
    movl 4(%esp), %edx
    movl $21, %eax
    int $0x80
    ret
.globl us_fd_open, us_fd_read, us_fd_write
us_fd_open:
    movl 8(%esp), %edx
    movl 4(%esp), %edi
    movl (%edx), %esi
    cmpl $1, %esi
    jl 3f
    cmpl $64, %esi
    jg 3f
    xorl %ecx, %ecx
1:  cmpl %esi, %ecx
    je 2f
    movl 4(%edx,%ecx,4), %eax
    testl %eax, %eax
    jz 2f
    cmpl $255, %eax
    ja 3f
    cmpl $63, %ecx
    je 3f
    movb %al, us_fd_path(%ecx)
    incl %ecx
    jmp 1b
2:  movb $0, us_fd_path(%ecx)
    movl $us_fd_path, %ebx
    movl %edi, %ecx
    movl $438, %edx
    movl $30, %eax
    int $0x80
    ret
3:  movl $-22, %eax
    ret
us_fd_read:
    movl 4(%esp), %ebx
    movl $us_fd_byte, %ecx
    movl $1, %edx
    movl $31, %eax
    int $0x80
    cmpl $1, %eax
    je 1f
    testl %eax, %eax
    jnz 2f
    movl $-1, %eax
    ret
1:  movzbl us_fd_byte, %eax
2:  ret
us_fd_write:
    movl 8(%esp), %ebx
    movl 4(%esp), %eax
    movb %al, us_fd_byte
    movl $us_fd_byte, %ecx
    movl $1, %edx
    movl $32, %eax
    int $0x80
    ret
.section .bss
us_fd_path: .skip 64
us_fd_byte: .skip 1
.section .note.GNU-stack,"",@progbits
