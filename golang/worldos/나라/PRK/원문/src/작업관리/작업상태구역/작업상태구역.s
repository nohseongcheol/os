#include "textflag.h"
#include "go_asm.h"


TEXT ·작업상태선택자적재(SB),NOSPLIT,$0
	MOVW p1+0(FP), AX
	BYTE $0x0F; BYTE $0x00; BYTE $0xD8; // ltr ax
	RET
	
