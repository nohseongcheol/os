#include "textflag.h"
#include "go_asm.h"

TEXT ·大域記述子表を搭載(SB),NOSPLIT,$0

	MOVL x+0(FP), DX
	BYTE $0x0f; BYTE $0x01; BYTE $0x12; // lgdt [edx]

        RET

