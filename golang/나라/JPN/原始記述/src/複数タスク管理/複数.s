#include "textflag.h"
#include "go_asm.h"

TEXT ·halt(SB),NOSPLIT,$0
        HLT;
        RET;

