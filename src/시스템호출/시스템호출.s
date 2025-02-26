//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"

TEXT ·M시스템호출_개입중단(SB),NOSPLIT,$8-24
        MOVL p1+0(FP), AX
        MOVL p2+4(FP), BX
        MOVL p3+8(FP), CX
        MOVL p4+12(FP), DX

        MOVL p5+16(FP), SI
        MOVL p6+20(FP), DI

        INT $0x80

        RET
