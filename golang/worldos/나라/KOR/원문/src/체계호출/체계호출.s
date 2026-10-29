#include "textflag.h"


TEXT ·I개입중단(SB),NOSPLIT,$0

	MOVL eax+0(FP), AX
	MOVL ebx+4(FP), BX
	MOVL ecx+8(FP), CX
	MOVL edx+12(FP), DX

	MOVL esi+16(FP), SI
	MOVL edi+20(FP), DI

	INT $0x80
	MOVL AX, ret+24(FP)
	RET

TEXT ·제어저장기3읽기(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, ret+0(FP)
	RET

	
