#include "textflag.h"
#include "go_asm.h"

TEXT ·SlåfraHeltal(SB),NOSPLIT,$0
	CLI
	RET
TEXT ·enter_usermode(SB),NOSPLIT,$0
	//PUSHL BP
	MOVL SP, BP
	//CLI

	//MOVL SP, 0(SP)
	//PUSHL $0x0
	//MOVL $runtime·g0(SB), 0(SP)
	//CALL ·udskrivesp(SB)
	//POPL AX

	//PUSHL $0x0
	//MOVL $runtime·m0(SB), 0(SP)
	//CALL ·udskrivesp(SB)
	//POPL AX

	//MOVL (TLS), AX
	//PUSHL AX
	//CALL ·udskrivesp(SB)
	//POPL AX


	//MOVL p1+0(FP), BX
	//MOVL p2+4(FP), CX
	//MOVL p3+8(FP), DX
	//MOVL $0x1ee000, $runtime·m0(SB)
	

	MOVL $0x28|3, AX
	MOVW AX, DS
	MOVW AX, ES
	MOVW AX, FS
	MOVW AX, GS


	PUSHL $0x28|3	// push ss3

	MOVL p2+4(FP), CX
	//MOVL SP, CX
	PUSHL CX	// push esp3
	//PUSHL AX

	PUSHFL		// push flags on stack
	POPL AX		// pop into eax
	ORL p3+8(FP), AX // copy eflags from args 3
	//MOVL p3+8(FP), AX // copy eflags from args 3
	//MOVL 0x200206, AX // copy eflags from args 3
	//ORL 0xC(BP), AX // copy eflags from args 3
	PUSHL AX


	PUSHL $0x20|3	// push cs, requests priv. level=3


	XORL AX, AX		// clear eax
	MOVL p1+0(FP), AX	// load new ip into eax
	//MOVL 0x4(BP), AX	// load new ip into eax

	//ADDL $0x12, AX
	PUSHL AX // push eip onto stack

	//PUSHL $0x0
	//MOVL SP, 0(SP)
	//CALL ·udskrivesp(SB)
	//POPL AX
	
	//MOVL $0x20|3, AX
	//MOVW AX, GS
	//HLT
	//ADDL $0x8, SP
	IRETL

TEXT ·jumpusermodeiret(SB),NOSPLIT,$0

	MOVL SP, BP
	CLI

	MOVL p1+4(FP), DI
	MOVL p1+8(FP), BX
	MOVL p1+12(FP), CX // send user process entry to shared library
	MOVL p1+16(FP), DX // send global offset table to shared library
	MOVL p1+20(FP), SI // send dynamic link-map to shared library

	ORL $0x202, BX
	ANDL $0xFFFF8FFF, BX

        MOVL $0x28|3, AX // 20|3 // 28|3
        MOVW AX, DS
        MOVW AX, ES
        MOVW AX, FS

        MOVW $0x30|3, AX
        MOVW AX, GS

	MOVL p1+0(FP), AX
	PUSHL $0x28|3 // push ss // 20|3 //28|3
	PUSHL DI // esp
	PUSHL BX  // eflags
	PUSHL $0x20|3 // cs // 18|3 //20|3
	PUSHL AX

	IRETL
TEXT ·jumpusermodeiret1(SB),NOSPLIT,$0
	RET

TEXT ·threadAfslutLøkkekolonier(SB),NOSPLIT,$0
	STI
	BYTE $0xF4
	BYTE $0xEB; BYTE $0xFD

TEXT ·enter_usermode_sysexit(SB),NOSPLIT,$0
	MOVL SP, BP
	CLI
	MOVL $0x20|3, AX

	MOVW AX, DS
	MOVW AX, ES
	MOVW AX, FS
	MOVW AX, GS

	XORL DX, DX
	//MOVL $0x100008, AX
	MOVL $0x8, AX
	MOVL $0x174, CX
	//BYTE $0x0f; BYTE $0x30; // wrmsr
	WRMSR
	
	//MOVL p1+0(FP), DX
	MOVL $UserModeTest(SB), DX
	//MOVL $0x0016ad50, DX
	MOVL SP, CX
	//MOVL $0x1e2258, DX
	//MOVL p2+4(FP), CX
	//HLT
	BYTE $0x0f; BYTE $0x35; // sysexit 
	RET
	

TEXT ·JumpUserMode(SB),NOSPLIT,$0
	POPL AX
	POPL GS
	POPL FS
	POPL ES
	POPL DS
	POPAL
	ADDL $8, SP
	IRETL


TEXT ·backupfpregs(SB),NOSPLIT,$0
    MOVL ·buffer_2+0(FP), AX
    FXSAVE (AX)
    RET

TEXT ·gendanfpregs(SB),NOSPLIT,$0
    MOVL ·buffer_2+0(FP), AX
    FXRSTOR (AX)
    RET

TEXT ·fxsave(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXSAVE (AX)
	RET
TEXT ·fxrstor(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXRSTOR (AX)
	RET

TEXT ·switchPageDir(SB),NOSPLIT,$0
	MOVL ·dir+0(FP), AX
	MOVL AX, CR3
	RET

TEXT ·getesp(SB),NOSPLIT,$0
        MOVL SP, ret+4(FP)
        RET

TEXT ·satcr3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET
TEXT ·getcr3(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·satds(SB),NOSPLIT,$0
    MOVL ds_segment+0(FP), AX
    MOVW AX, DS
    RET

TEXT ·satgs(SB),NOSPLIT,$0
    MOVL gs_segment+0(FP), AX
    MOVW AX, GS
    RET
