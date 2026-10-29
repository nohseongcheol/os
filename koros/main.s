//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"
#include "go_asm.h"

TEXT ·멈추기(SB),NOSPLIT,$0
	HLT;
	RET;
TEXT ·getESP(SB),NOSPLIT,$0
        MOVL SP, ret+4(FP)
        RET
