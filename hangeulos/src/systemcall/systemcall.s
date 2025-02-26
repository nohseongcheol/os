#include "textflag.h"


TEXT ·Interrupt(SB),NOSPLIT,$0

	MOVL p1+0(FP), AX
	MOVL p2+4(FP), BX
	MOVL p3+8(FP), CX
	MOVL p4+12(FP), DX

	MOVL p5+16(FP), SI
	MOVL p6+20(FP), DI

	INT $0x80
	RET

	
