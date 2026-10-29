#include "textflag.h"
#include "go_tls.h"
#include "go_asm.h"


TEXT ·halt(SB),NOSPLIT,$0
	HLT;
	RET;

TEXT ·morestack(SB),NOSPLIT,$0
	BYTE $0x65; BYTE $0x8b; BYTE $0x0d; BYTE $0x00; BYTE $0x00; BYTE $0x00; BYTE $0x00;
	MOVL -4(CX), CX
	//MOVL $0x0, AX
	//MOVL AX, 8(CX)
	//MOVL $0x05, AX
	//MOVL $0x04, BX
	//CMPL AX, BX
	//JBE EXIT
	MOVL 8(CX), AX
	PUSHL $0x0
	MOVL CX, 0(SP)
	CALL ·printreg(SB)
	POPL AX
	//HLT
	CALL runtime·morestack_noctxt(SB)
EXIT:
        RET;

TEXT ·getesp(SB),NOSPLIT,$0
	MOVL SP, ret+0(FP)
	RET

TEXT ·getesi(SB),NOSPLIT,$0
	MOVL SI, ret+0(FP)
	RET

TEXT ·getgs(SB),NOSPLIT,$0
	MOVW GS, ret+4(FP)
	RET
TEXT ·P暂停loop(SB), NOSPLIT, $0
	PAUSE_LOOP:
	MOVL $0x1, AX
	CMPL AX, $0x1
	JE PAUSE_LOOP
	RET

TEXT ·gettls(SB),NOSPLIT,$0
	//MOVL 0(GS), AX
	get_tls(CX)
	MOVL g(CX), BX	
	MOVL BX, ret+0(FP)
	RET;

TEXT ·任务d(SB),NOSPLIT,$0
        //BYTE $0x65; BYTE $0x8b; BYTE $0x0d; BYTE $0x00; BYTE $0x00; BYTE $0x00; BYTE $0x00;
        //MOVL -0x4(CX), CX
	//SUBL 0x44, SP
	MOVB $0x40, AX
	LOOP1:
		ADDL $0x1, AX
		MOVB AX, 0xB8074
		//MOVL $0x04, AX
		//INT $0x20
		//INT $0x81
		//CALL ·任务d1(SB)
	JMP LOOP1
	RET

TEXT ·任务F(SB),NOSPLIT,$0
	PUSHL BP
	MOVL SP, BP
LOOP2:
	MOVB $0x4E, 0xB8072
	MOVB $0x4E, 0xB8074
	//ADDL $0x500000, SP
	//MOVL SP, 0(SP)
	//CALL main·printreg(SB)
	//HLT
	MOVL $0x08, AX
	MOVL $0x06, BX
	//INT $0x80
	JMP LOOP2
	MOVL BP, SP
	POPL BP
	RET

TEXT ·R重新载入cr3(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, CR3
	MOVL AX, ret+0(FP)
	RET

TEXT ·Getcr2(SB),NOSPLIT,$0
        MOVL CR2, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·Getcr3(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·S集合cr3(SB),NOSPLIT,$0
	MOVL cr3+0(FP), AX
	MOVL AX, CR3
	RET

TEXT ·Getcr0(SB),NOSPLIT,$0
	MOVL CR0, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·Getcr4(SB),NOSPLIT,$0
	MOVL CR4, AX
	MOVL AX, ret+0(FP)
	RET
TEXT ·E启用分页管理(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000001, AX
    MOVL AX, CR0
    RET


TEXT ·P打印(SB),NOSPLIT,$0
	MOVB $0x4E, 0xC00b8004
	RET

TEXT ·SetValue(SB),NOSPLIT,$0
	MOVL v+0(FP), AX
	MOVL addr+4(FP), BX
	MOVL AX, 0(BX)	
	RET

TEXT ·Get值(SB),NOSPLIT,$0
	MOVL addr+0(FP), BX
	//MOVL (BX), AX
	MOVL BX, ret+4(FP)
	RET

