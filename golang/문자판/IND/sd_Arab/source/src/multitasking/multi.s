#include "textflag.h"
#include "go_asm.h"

TEXT ·멈추기(SB),NOSPLIT,$0
        HLT;
        RET;

