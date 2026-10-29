//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"
#include "go_asm.h"

TEXT ·공용서술자표_올리기(SB),NOSPLIT,$0

	MOVL x+0(FP), DX
	BYTE $0x0f; BYTE $0x01; BYTE $0x12; // lgdt [edx]
        RET

