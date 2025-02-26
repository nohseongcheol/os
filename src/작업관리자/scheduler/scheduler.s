#include "textflag.h"
#include "go_asm.h"

TEXT ·DisableInt(SB),NOSPLIT,$0
	CLI
	RET

TEXT ·fxsave(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXSAVE 0(AX)
	RET

TEXT ·fxrstor(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXRSTOR 0(AX)
	RET

TEXT ·enter_usermode(SB),NOSPLIT,$0
	//PUSHL BP
	CLI

	//MOVL SP, 0(SP)
	//PUSHL $0x0
	//MOVL $runtime·g0(SB), 0(SP)
	//CALL ·printESP(SB)
	//POPL AX

	//PUSHL $0x0
	//MOVL $runtime·m0(SB), 0(SP)
	//CALL ·printESP(SB)
	//POPL AX

	//MOVL (TLS), AX
	//PUSHL AX
	//CALL ·printESP(SB)
	//POPL AX


	//MOVL p1+0(FP), BX
	//MOVL p2+4(FP), CX
	//MOVL p3+8(FP), DX
	//MOVL $0x1ee000, $runtime·m0(SB)
	

	MOVL $0x20|3, AX
	MOVW AX, DS
	MOVW AX, ES
	//MOVW AX, FS
	//MOVW AX, GS


	PUSHL $0x20|3	// push ss3

	MOVL p2+4(FP), CX
	//MOVL SP, CX
	PUSHL (CX)	// push esp3
	//PUSHL AX

	PUSHFL		// push flags on stack
	POPL AX		// pop into eax
	ORL p3+8(FP), AX // copy eflags from args 3
	//MOVL p3+8(FP), AX // copy eflags from args 3
	//MOVL 0x200206, AX // copy eflags from args 3
	//ORL 0xC(BP), AX // copy eflags from args 3
	PUSHL AX


	PUSHL $0x18|3	// push cs, requests priv. level=3


	XORL AX, AX		// clear eax
	MOVL p1+0(FP), AX	// load new ip into eax
	//MOVL 0x4(BP), AX	// load new ip into eax

	//ADDL $0x12, AX
	PUSHL AX // push eip onto stack

	//PUSHL $0x0
	//MOVL SP, 0(SP)
	//CALL ·printESP(SB)
	//POPL AX
	
	//MOVL $0x20|3, AX
	//MOVW AX, GS
	//HLT
	//ADDL $0x8, SP
	IRETL

TEXT ·enter_usermode_sysexit(SB),NOSPLIT,$0
	MOVL SP, BP
	CLI
	MOVL $0x20|3, AX

	MOVW AX, DS
	MOVW AX, ES
	MOVW AX, FS
	MOVW AX, GS

	XORL DX, DX
	MOVL $0x100008, AX
	MOVL $0x174, CX
	//BYTE $0x0f; BYTE $0x30; // wrmsr
	WRMSR
	
	MOVL p1+0(FP), DX
	//MOVL $0x1e2258, DX
	MOVL p2+4(FP), CX
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
