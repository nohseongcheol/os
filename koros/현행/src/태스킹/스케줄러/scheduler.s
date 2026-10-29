#include "textflag.h"
#include "go_asm.h"

TEXT ·D디아이에스에이비엘이아이엔티(SB),NOSPLIT,$0
	CLI
	RET
TEXT ·이nter_usermode(SB),NOSPLIT,$0
	//PUSHL BP
	MOVL SP, BP
	//CLI

	//MOVL SP, 0(SP)
	//PUSHL $0x0
	//MOVL $runtime·지0(SB), 0(SP)
	//CALL ·피알아이엔티이에스피(SB)
	//POPL AX

	//PUSHL $0x0
	//MOVL $runtime·m0(SB), 0(SP)
	//CALL ·피알아이엔티이에스피(SB)
	//POPL AX

	//MOVL (TLS), AX
	//PUSHL AX
	//CALL ·피알아이엔티이에스피(SB)
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
	//CALL ·피알아이엔티이에스피(SB)
	//POPL AX
	
	//MOVL $0x20|3, AX
	//MOVW AX, GS
	//HLT
	//ADDL $0x8, SP
	IRETL

TEXT ·제이유엠피유에스이알엠오디이아이알이티(SB),NOSPLIT,$0

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
TEXT ·제이유엠피유에스이알엠오디이아이알이티1(SB),NOSPLIT,$0
	RET

TEXT ·스레드엑시트엘오오피(SB),NOSPLIT,$0
	STI
	BYTE $0xF4
	BYTE $0xEB; BYTE $0xFD

TEXT ·이nter_usermode_sysexit(SB),NOSPLIT,$0
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


TEXT ·비에이시케이유피에프피알이지에스(SB),NOSPLIT,$0
    MOVL ·버퍼+0(FP), AX
    FXSAVE (AX)
    RET

TEXT ·알이에스티오알이에프피알이지에스(SB),NOSPLIT,$0
    MOVL ·버퍼+0(FP), AX
    FXRSTOR (AX)
    RET

TEXT ·에프엑스에스에이브이이(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXSAVE (AX)
	RET
TEXT ·에프엑스알에스티오알(SB),NOSPLIT,$0
	MOVL p1+0(FP), AX
	FXRSTOR (AX)
	RET

TEXT ·에스witchPageDir(SB),NOSPLIT,$0
	MOVL ·dir+0(FP), AX
	MOVL AX, CR3
	RET

TEXT ·겟이에스피(SB),NOSPLIT,$0
        MOVL SP, ret+4(FP)
        RET

TEXT ·셋시에이알3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET
TEXT ·겟시에이알3(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·셋디에스(SB),NOSPLIT,$0
    MOVL ds_segment+0(FP), AX
    MOVW AX, DS
    RET

TEXT ·셋지에스(SB),NOSPLIT,$0
    MOVL gs_segment+0(FP), AX
    MOVW AX, GS
    RET
