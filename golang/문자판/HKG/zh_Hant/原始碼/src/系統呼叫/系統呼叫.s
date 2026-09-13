#include "textflag.h"


TEXT ·I中斷(SB),NOSPLIT,$0

	MOVL eax+0(FP), AX
	MOVL ebx+4(FP), BX
	MOVL ecx+8(FP), CX
	MOVL edx+12(FP), DX

	MOVL esi+16(FP), SI
	MOVL edi+20(FP), DI

	INT $0x80
	MOVL AX, ret+24(FP)
	RET

TEXT ·getcr3(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, ret+0(FP)
	RET

	
