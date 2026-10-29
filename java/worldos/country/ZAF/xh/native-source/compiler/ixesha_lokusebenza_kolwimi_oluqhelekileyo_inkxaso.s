.code32
.section .bss
.balign 16
heap_start: .skip 262144
heap_end:
heap_cursor: .long 0

.text
# 내부 ABI: eax=ULUHLU_ixabiso, ecx=umbhalo_omncinane_ixabiso. 성공 시 eax/ecx/edx를 보존한다.
.globl rt_array_check
rt_array_check:
    testl %eax, %eax
    jz rt_null
    cmpl (%eax), %ecx
    jae rt_bounds
    ret

.globl rt_new_array
rt_new_array:
    testl %eax, %eax
    js rt_negative_size
    cmpl $65535, %eax
    ja rt_out_of_memory
    movl %eax, %edx
    leal 4(,%eax,4), %ecx
    movl heap_cursor, %ebx
    addl %ebx, %ecx
    cmpl $262144, %ecx
    ja rt_out_of_memory
    movl %ecx, heap_cursor
    leal heap_start(%ebx), %eax
    movl %edx, (%eax)
    # 영역은 BSS에서 한 번만 할당되므로 모든 원소는 0이다. vulela_Ugcino/GC는 없다.
    ret

.globl rt_heap_used
rt_heap_used:
    movl heap_cursor, %eax
    ret

.globl rt_div_zero, rt_null, rt_bounds, rt_negative_size, rt_out_of_memory
rt_div_zero:
    movl $1, %eax
    jmp rt_panic
rt_null:
    movl $2, %eax
    jmp rt_panic
rt_bounds:
    movl $3, %eax
    jmp rt_panic
rt_negative_size:
    movl $4, %eax
    jmp rt_panic
rt_out_of_memory:
    movl $5, %eax
    jmp rt_panic
.section .note.GNU-stack,"",@progbits
