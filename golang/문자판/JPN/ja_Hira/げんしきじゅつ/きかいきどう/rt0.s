; vim: set ft=nasm :
%include "ていすう.inc"

section .bss

;--------------------------------------------------------------------
; Reserve 3 pages for the initial page tables
page_table_l4:		resb 4096
page_table_l3:		resb 4096
page_table_l2:		resb 4096

;--------------------------------------------------------------------
align 4

multiboot_data: resb 16384

; Reserve 16K for our stack. Stacks should be aligned to 16 byte boundaries.
stack_bottom:
	;resb 1638400; 1600 KiB
	;resb 1638400; 1600 KiB
	;resb 1638400; 1600 KiB
	;resb 1638400; 1600 KiB
	;resb 0x4000;
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
	resb 16384; 16 KiB
stack_top:

; According to the "ELF handling for TLS" document section 4.3.2
; (https://www.akkadia.org/drepper/tls.pdf) for the GNU variant of the IA-32 ABI, 
; gs:0x00 contains a pointer to the TCB. Variables in the TLS are stored 
; before the TCB and are accessed using negative offsets from the TCB address.
g0_ptr:	        resd 1 
tcb_ptr:        resd 1 

;------------------------------------------------------------------------------
global KERNEL_VIRTUAL_BASE
KERNEL_VIRTUAL_BASE equ 0xC0000000                  ; 3GB
KERNEL_PAGE_NUMBER equ (KERNEL_VIRTUAL_BASE >> 22)  ; Page directory index of kernel's 4MB PTE.

section .data
align 0x1000
global BootPageDirectory:
BootPageDirectory:
    ; This page directory entry identity-maps the first 4MB of the 32-bit physical address space.
    ; All bits are clear except the following:
    ; bit 7: PS The kernel page is 4MB.
    ; bit 1: RW The kernel page is read/write.
    ; bit 0: P  The kernel page is present.
    ; This entry must be here -- otherwise the kernel will crash immediately after paging is
    ; enabled because it can't fetch the next instruction! It's ok to unmap this page later.
	;mov eax, 0xFFFF0000
	;mov eax, BootPageTable
	;mov eax, 0x00000013
	;mov [BootPageDirectory+4], eax
    ;dd 0x001ee083
    dd 0x00000083
    ;times (KERNEL_PAGE_NUMBER - 1) dd 0x00000083                 ; Pages before kernel space.
    times (KERNEL_PAGE_NUMBER - 1) dd 0				  ; Pages before kernel space.
    ; This page directory entry defines a 4MB page containing the kernel.
    times (1024) dd 0x00000083
    times (1024 - KERNEL_PAGE_NUMBER - 1) dd 0  ; Pages after the kernel image.
BootPageTable:
    times (1024*1024) dd 0x00000083
    ;times (1024 - KERNEL_PAGE_NUMBER - 1) dd 0x00000083  ; Pages after the kernel image.
;------------------------------------------------------------------------------

section .text
bits 32
align 4

MULTIBOOT_MAGIC equ 0x36d76289

;G_STACK_LO equ 0x0
;G_STACK_HI equ 0x4
;G_STACKGUARD0 equ 0x8

err_unsupported_bootloader db '[rt0] kernel not loaded by multiboot-compliant bootloader', 0

tmp_multiboot_info dw 0


;------------------------------------------------------------------------------
; Kernel arch-specific entry point
;
; The boot loader will jump to this symbol after setting up the CPU according
; to the multiboot standard. At this point:
; - A20 is enabled
; - The CPU is using 32-bit protected mode
; - Interrupts are disabled
; - Paging is disabled
; - EAX contains the magic value ‘0x36d76289’; the presence of this value indicates
;   to the operating system that it was loaded by a Multiboot-compliant boot loader
; - EBX contains the 32-bit physical address of the Multiboot information structure
;------------------------------------------------------------------------------

section .multiboot_header
global _rt0_entry
_rt0_entry:


	;cmp eax, MULTIBOOT_MAGIC
	;jne unsupported_bootloader

	; Initalize our stack by pointing ESP to the BSS-allocated stack. In x86,
	; stack grows downwards so we need to point ESP to stack_top
	;call _rt0_populate_initial_page_tables
	;call _rt0_enable_paging

	call _rt0_32_setup_go_runtime_structs

	mov esp, stack_top - PAGE_OFFSET


	; Enable SSE/AVX
	call _rt0_enable_sse

 	; Load initial GDT
 	call _rt0_load_gdt

	; init g0 so we can invoke Go functions. For now we use hardcoded offsets 
	; that correspond to the g struct definition in src/runtime/runtime2.go
	; jump into the go code
 	
	;lgdt [done]

	; Enable Paging
	;call _rt0_populate_initial_page_tables
	;call _rt0_enter_long_mode


	;jmp _rt0_enable_paging
	;hlt



	push stack_bottom
	push stack_top
	;mov ebx, [tmp_multiboot_info]
	mov ebx, BootPageDirectory
    	push ebx


	extern kernel.KKernelEntry
	call kernel.KKernelEntry

	; Main should never return; halt the CPU
halt:
	cli
	hlt

_rt0_32_entry:
	; Provide a stack 
	mov esp, stack_top- PAGE_OFFSET

	; Ensure we were booted by a bootloader supporting multiboot
	cmp eax, 0x36d76289
	jne _rt0_32_entry.unsupported_bootloader

	; Copy multiboot struct to our own buffer
	call _rt0_copy_multiboot_data
	

	; Check processor features
	call _rt0_check_cpuid_support
	call _rt0_check_longmode_support
	call _rt0_check_sse_support

	; Setup initial page tables, enable paging and enter longmode 
	call _rt0_populate_initial_page_tables
	call _rt0_enter_long_mode

        push stack_bottom
        push stack_top
        mov ebx, [tmp_multiboot_info]
        push ebx

        extern kernel.KKernelEntry
        jmp CS_SEG:kernel.KKernelEntry


.unsupported_bootloader:
	mov edi, err_unsupported_bootloader - PAGE_OFFSET
	call write_string
	jmp _rt0_32_entry.halt

.halt:
	cli
	hlt

unsupported_bootloader:
	mov edi, err_unsupported_bootloader
	call write_string
	jmp _rt0_32_entry.halt

.end:

_rt0_32_setup_go_runtime_structs:
	%include "goasmoffset.inc"

	extern runtime.physPageSize
	mov eax, runtime.physPageSize
	mov dword [eax], 0x1000 ; 4096


	extern runtime.g0
	mov esi, runtime.g0
	mov dword [esi + GO_G_STACK+GO_STACK_LO], stack_bottom
	mov dword [esi + GO_G_STACK+GO_STACK_HI], stack_top
	mov dword [esi + GO_G_STACKGUARD0], stack_bottom
	;mov dword [esi + GO_G_STACKGUARD1], stack_bottom


	extern runtime.m0
	mov ebx, runtime.m0
	mov dword [ebx+GO_M_CURG], esi
	mov dword [ebx+GO_M_G0], esi
	mov dword [esi+GO_G_M], stack_top
	
		

	mov dword [g0_ptr], esi

	mov eax, tcb_ptr
	mov dword [eax], eax

	mov ecx, 0xc0000100
	mov esi, tcb_ptr
	mov eax, esi
	shr esi, 16
	mov edx, esi
	wrmsr

	ret

;------------------------------------------------------------------------------
; Write the NULL-terminated string contained in edi to the screen using white
; text on red background.  Assumes that text-mode is enabled and that its
; physical atdress is 0xb8000.
;------------------------------------------------------------------------------
write_string:
	push eax
	push ebx

	mov ebx,0xb8000
	mov ah, 0x4F
next_char:
	mov al, byte[edi]
	test al, al
	jz done

	mov word [ebx], ax
	add ebx, 2
	inc edi
	jmp next_char

done:
	pop ebx
	pop eax
	ret


;------------------------------------------------------------------------------
; Load GDT and flush CPU caches
;------------------------------------------------------------------------------

_rt0_load_gdt:
	push eax
	push ebx


	; Store the address to the TCB in tcb_ptr
	; and set up gs base address to it
	mov eax, tcb_ptr
	mov [tcb_ptr], eax
	mov ebx, gdt0_gs_seg
	mov [ebx+2], al
	mov [ebx+3], ah
	shr eax, 16
	mov [ebx+4], al


	;;lgdt [gdt0_desc]
	;;lgdt [_rt0_entry]
	;;lgdt [done]
	lgdt [gdt0_desc]

	; GDT has been loaded but the CPU still has the previous GDT data in cache.
	; We need to manually update the descriptors and use a JMP command to set
	; the CS segment descriptor
	jmp CS_SEG:update_descriptors
update_descriptors:
	mov ax, DS_SEG
	mov ds, ax
	mov es, ax
	mov fs, ax
	mov ss, ax
	mov ax, GS_SEG
	mov gs, ax

	pop ebx
	pop eax
	ret

;------------------------------------------------------------------------------
; GDT definition
;------------------------------------------------------------------------------
%include "gdt.inc"

align 2
gdt0:

gdt0_nil_seg: GDT_ENTRY_32 0x00, 0x0, 0x0, 0x0				        ; nil descriptor (not used by CPU but required by some emulators)
gdt0_cs_seg:  GDT_ENTRY_32 0x00, 0xFFFFF, SEG_EXEC | SEG_R, SEG_GRAN_4K_PAGE    ; code descriptor
gdt0_ds_seg:  GDT_ENTRY_32 0x00, 0xFFFFF, SEG_NOEXEC | SEG_W, SEG_GRAN_4K_PAGE  ; data descriptor
gdt0_gs_seg:  GDT_ENTRY_32 0x00, 0xFFFFF, SEG_NOEXEC | SEG_W, SEG_GRAN_BYTE        ; TLS descriptor (required in order to use go segmented stacks)

gdt0_desc:
	dw gdt0_desc - gdt0 - 1  ; gdt size should be 1 byte less than actual length
	dd gdt0

NULL_SEG equ gdt0_nil_seg - gdt0
CS_SEG   equ gdt0_cs_seg - gdt0
DS_SEG   equ gdt0_ds_seg - gdt0
GS_SEG   equ gdt0_gs_seg - gdt0

;------------------------------------------------------------------------------
; Enable SSE support. Code taken from:
; http://wiki.osdev.org/SSE#Checking_for_SSE
;------------------------------------------------------------------------------
_rt0_enable_sse:
	push eax

	; check for SSE
	mov eax, 0x1
	cpuid
	test edx, 1<<25
	jz .no_sse

	; enable SSE
	mov eax, cr0
	and ax, 0xFFFB      ; clear coprocessor emulation CR0.EM
	or ax, 0x2          ; set coprocessor monitoring  CR0.MP
	mov cr0, eax
	mov eax, cr4
	or ax, 3 << 9       ; set CR4.OSFXSR and CR4.OSXMMEXCPT at the same time
	mov cr4, eax

	pop eax
	ret
.no_sse:
	cli
	hlt

;-------------------------------------------------------------------------------
_rt0_copy_multiboot_data:
	mov esi, ebx
	mov edi, multiboot_data - PAGE_OFFSET

	mov ecx, dword [esi]
	;cmp ecx, 16384
	cmp ecx, 1638400*4
	jle _rt0_copy_multiboot_data.copy

	mov edi, err_multiboot_data_too_big - PAGE_OFFSET
	call write_string
	jmp _rt0_32_entry.halt

.copy:
	test ecx, ecx
	jz _rt0_copy_multiboot_data.done

	mov eax, dword[esi]
	mov dword [edi], eax
	add esi, 4
	add edi, 4
	sub ecx, 4
	jmp _rt0_copy_multiboot_data.copy

.done:
	ret
;-------------------------------------------------------------------------------
;------------------------------------------------------------------------------
; Check that the processor supports the CPUID instruction.
; 
; To check if CPUID is supported, we need to attempt to flip the ID bit (bit 21)
; in the FLAGS register. If that works, CPUID is available.
;
; Code taken from: http://wiki.osdev.org/Setting_Up_Long_Mode#x86_or_x86-64
;------------------------------------------------------------------------------
_rt0_check_cpuid_support:
	; Copy FLAGS in to EAX via stack
	pushfd
	pop eax

	; Copy to ECX as well for comparing later on
	mov ecx, eax

	; Flip the ID bit
	xor eax, 1 << 21

	; Copy EAX to FLAGS via the stack
	push eax
	popfd

	; Copy FLAGS back to EAX (with the flipped bit if CPUID is supported)
	pushfd
	pop eax

	; Restore FLAGS from the old version stored in ECX (i.e. flipping the
	; ID bit back if it was ever flipped).
	push ecx
	popfd

	; Compare EAX and ECX. If they are equal then that means the bit
	; wasn't flipped, and CPUID isn't supported.
	cmp eax, ecx
	je _rt0_check_cpuid_support.no_cpuid
	ret

.no_cpuid:
	mov edi, err_cpuid_not_supported - PAGE_OFFSET
	call write_string
	jmp _rt0_32_entry.halt

;------------------------------------------------------------------------------
; Check that the processor supports long mode
; Code taken from: http://wiki.osdev.org/Setting_Up_Long_Mode#x86_or_x86-64
;------------------------------------------------------------------------------
_rt0_check_longmode_support:
	; To check for longmode support we need to ensure that the CPUID instruction
	; can report it. To do this we need to query it first.
	mov eax, 0x80000000    ; Set the A-register to 0x80000000.
	cpuid
	cmp eax, 0x80000001    ; We need at least 0x80000001 to check for long mode.
	jb _rt0_check_longmode_support.no_long_mode

	mov eax, 0x80000001    ; Set the A-register to 0x80000001.
	cpuid
	test edx, 1 << 29      ; Test if the LM-bit, which is bit 29, is set in the D-register.
	jz _rt0_check_longmode_support.no_long_mode
	ret

.no_long_mode:
	mov edi, err_longmode_not_supported - PAGE_OFFSET
	call write_string
	jmp _rt0_32_entry.halt

;------------------------------------------------------------------------------
; Check for and enabl SSE support. Code taken from:
; http://wiki.osdev.org/SSE#Checking_for_SSE
;------------------------------------------------------------------------------
_rt0_check_sse_support:
	; check for SSE
	mov eax, 0x1
	cpuid
	test edx, 1<<25
	jz _rt0_check_sse_support.no_sse

	; Enable SSE
	mov eax, cr0
	and ax, 0xfffb      ; Clear coprocessor emulation CR0.EM
	or ax, 0x2          ; Set coprocessor monitoring  CR0.MP
	mov cr0, eax
	mov eax, cr4
	or ax, 3 << 9       ; Set CR4.OSFXSR and CR4.OSXMMEXCPT at the same time
	mov cr4, eax

	ret
.no_sse:
	mov edi, err_sse_not_supported - PAGE_OFFSET
	call write_string
	jmp _rt0_32_entry.halt

PAGE_PRESENT  equ (1 << 0)
PAGE_WRITABLE equ (1 << 1)
PAGE_2MB     equ (1 << 7)

_rt0_populate_initial_page_tables:
	; The CPU uses bits 39-47 of the virtual address as an index to the P4 table.
	mov eax, page_table_l3 - PAGE_OFFSET
	or eax, PAGE_PRESENT | PAGE_WRITABLE
	mov ebx, page_table_l4 - PAGE_OFFSET
	mov [ebx], eax 
	
	; Recursively map the last P4 entry to itself. This allows us to use 
	; specially crafted memory addresses to access the page tables themselves
	mov ecx, ebx 
	or ecx, PAGE_PRESENT | PAGE_WRITABLE 
	mov [ebx + 511*8], ecx

	; Also map the addresses starting at PAGE_OFFSET to the same P3 table. 
	; To find the P4 index for PAGE_OFFSET we need to extract bits 39-47
	; of its address.
	mov ecx, (PAGE_OFFSET >> 39) & 511
	mov [ebx + ecx*8], eax 

	; The CPU uses bits 30-38 as an index to the P3 table. We just need to map 
	; entry 0 from the P3 table to point to the P2 table .
	mov eax, page_table_l2 - PAGE_OFFSET
	or eax, PAGE_PRESENT | PAGE_WRITABLE 
	mov ebx, page_table_l3 - PAGE_OFFSET
	mov [ebx], eax 

	; For the L2 table we enable the huge page bit which allows us to specify 
	; 2M pages without needing to use the L1 table. To cover the required 
	; 0-8M region we need to provide 4 2M page entries at indices 0 to 4.
	mov ecx, 0
	mov ebx, page_table_l2 - PAGE_OFFSET
.next_page:
	mov eax, 1 << 21  ; 2M
	mul ecx           ; eax *= ecx
	or eax, PAGE_PRESENT | PAGE_WRITABLE | PAGE_2MB
	mov [ebx + ecx*8], eax

	inc ecx 
	cmp ecx, 4
	jne _rt0_populate_initial_page_tables.next_page

	ret
_rt0_enter_long_mode:
	; Load page table map pointer to cr3
	mov eax, page_table_l4 - PAGE_OFFSET
	mov cr3, eax  


	; Enable PAE support 
	mov eax, cr4 
	or eax, 1 << 5
	mov cr4, eax

	; Now enable long mode (bit 8) and the no-execute support (bit 11) by 
	; modifying the EFER MSR
	mov ecx, 0xc0000080
	rdmsr	; read msr value to eax
	or eax, (1 << 8) | (1<<11)
	wrmsr


	; Finally enable paging (bit 31) and user/kernel page write protection (bit 16)
	mov eax, cr0
	or eax, (1 << 31) | (1<<16)
	mov cr0, eax


	; We are in 32-bit compatibility submode. We need to load a 64bit GDT 
	; and perform a far jmp to switch to long mode
	mov eax, gdt0_desc - PAGE_OFFSET
	lgdt [eax]

	; set ds and es segments
	; to set the cs segment we need to perform a far jmp
	mov ax, DS_SEG
	mov ds, ax
	mov es, ax
	mov fs, ax
	mov gs, ax
	mov ss, ax

	jmp CS_SEG:.flush_gdt - PAGE_OFFSET


	
.flush_gdt:
	ret

_rt0_enable_paging:
	;Enable Paging START


       	; NOTE: Until paging is set up, the code must be position-independent and use physical
       	; addresses, not virtual ones!
       	mov ecx, (BootPageDirectory - KERNEL_VIRTUAL_BASE)
       	;mov ecx, BootPageDirectory
       	mov cr3, ecx                                        ; Load Page Directory Base Register.

	;call _rt0_populate_initial_page_tables
	;mov ecx, page_table_l4 - PAGE_OFFSET
	;mov cr3, ecx


	;call a20_kbc

        mov ecx, cr4
        or ecx, 0x00000010                          ; Set PSE bit in CR4 to enable 4MB pages.
	;or ecx, 1<<5
        mov cr4, ecx

	;hlt

	mov ecx, cr0
        or ecx, 0x80000001                          ; Set PG bit in CR0 to enable paging.
	;or ecx, (1 << 31) | (1<<16)
        mov cr0, ecx

    	lea ecx, [higher_half_start]
    	jmp ecx   

higher_half_start:

        mov dword [BootPageDirectory], 0
        invlpg [0]

	hlt

        mov esp, stack_bottom
        ;mov esp, stack_bottom - PAGE_OFFSET

	;push eax
	;mov eax, tcb_ptr
	;mov [tcb_ptr], eax
	;mov ebx, gdt0_gs_seg


        call _rt0_32_setup_go_runtime_structs
        ;mov esp, stack_top - PAGE_OFFSET


        ; Enable SSE/AVX 
        call _rt0_enable_sse

        ; Load initial GDT
        call _rt0_load_gdt
	;;mov eax, gdt0_desc

	
	mov byte[0xC00b8002], 0x4D


        push stack_bottom
        push stack_top
        ;;mov ebx, [tmp_multiboot_info]
        mov edi, BootPageDirectory
        push edi 

        extern kernel.KKernelEntry
	;jmp 0x10:0x0006d140
	;jmp CS_SEG:kernel.KKernelEntry
        ;extern kernel.KKernelEntry
	;hlt
	call kernel.KKernelEntry

a20_kbc:
	mov al, 0xD1
	out 0x64, al

	mov al, 0xDF
	out 0x60, al
	ret

empty_8042:
	push ecx
	mov ecx, 100000	

_main:
	cli
	hlt

	ret	
section .data
;------------------------------------------------------------------------------
; Error messages
;------------------------------------------------------------------------------
err_multiboot_data_too_big db '[rt0_32] multiboot information data length exceeds local buffer size', 0
err_cpuid_not_supported db '[rt0_32] the processor does not support the CPUID instruction', 0
err_longmode_not_supported db '[rt0_32] the processor does not support longmode which is required by this kernel', 0
err_sse_not_supported db '[rt0_32] the processor does not support SSE instructions which are required by this kernel', 0


