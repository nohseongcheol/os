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
	CALL ·저장기상태출력(SB)
	POPL AX
	//HLT
	CALL runtime·morestack_noctxt(SB)
EXIT:
        RET;

TEXT ·쌓임공간꼭대기주소읽기(SB),NOSPLIT,$0
	MOVL SP, ret+0(FP)
	RET

TEXT ·원본주소저장기읽기(SB),NOSPLIT,$0
	MOVL SI, ret+0(FP)
	RET

TEXT ·추가구간선택자읽기(SB),NOSPLIT,$0
	MOVW GS, ret+4(FP)
	RET
TEXT ·F반복대기(SB), NOSPLIT, $0
	PAUSE_LOOP:
	MOVL $0x1, AX
	CMPL AX, $0x1
	JE PAUSE_LOOP
	RET

TEXT ·실행흐름지역주소읽기(SB),NOSPLIT,$0
	//MOVL 0(GS), AX
	get_tls(CX)
	MOVL g(CX), BX	
	MOVL BX, ret+0(FP)
	RET;

TEXT ·작업d(SB),NOSPLIT,$0
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
		//CALL ·작업d1(SB)
	JMP LOOP1
	RET

TEXT ·작업F(SB),NOSPLIT,$0
	PUSHL BP
	MOVL SP, BP
LOOP2:
	MOVB $0x4E, 0xB8072
	MOVB $0x4E, 0xB8074
	//ADDL $0x500000, SP
	//MOVL SP, 0(SP)
	//CALL main·저장기상태출력(SB)
	//HLT
	MOVL $0x08, AX
	MOVL $0x06, BX
	//INT $0x80
	JMP LOOP2
	MOVL BP, SP
	POPL BP
	RET

TEXT ·F주소변환캐시갱신(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, CR3
	MOVL AX, ret+0(FP)
	RET

TEXT ·F제어저장기2읽기(SB),NOSPLIT,$0
        MOVL CR2, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·F제어저장기3읽기(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·F제어저장기3쓰기(SB),NOSPLIT,$0
	MOVL cr3+0(FP), AX
	MOVL AX, CR3
	RET

TEXT ·F제어저장기0읽기(SB),NOSPLIT,$0
	MOVL CR0, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·F제어저장기4읽기(SB),NOSPLIT,$0
	MOVL CR4, AX
	MOVL AX, ret+0(FP)
	RET
TEXT ·F기억쪽관리활성화(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000001, AX
    MOVL AX, CR0
    RET


TEXT ·P출력(SB),NOSPLIT,$0
	MOVB $0x4E, 0xC00b8004
	RET

TEXT ·SetValue(SB),NOSPLIT,$0
	MOVL v+0(FP), AX
	MOVL addr+4(FP), BX
	MOVL AX, 0(BX)	
	RET

TEXT ·F주소의32비트값읽기(SB),NOSPLIT,$0
	MOVL addr+0(FP), BX
	//MOVL (BX), AX
	MOVL BX, ret+4(FP)
	RET

