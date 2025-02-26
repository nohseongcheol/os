#include "textflag.h"
#include "go_asm.h"


TEXT ·flush_tss(SB),NOSPLIT,$0
	MOVW p1+0(FP), AX
	BYTE $0x0F; BYTE $0x00; BYTE $0xD8; // ltr ax
	RET
	
