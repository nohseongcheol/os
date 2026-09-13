#include "textflag.h"

TEXT ·enablePaging(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000000, AX
    MOVL AX, CR0
    RET

TEXT ·switchPageDir(SB),NOSPLIT,$0
    MOVL ·dir+0(FP), AX
    MOVL AX, CR3
    RET

TEXT ·getCurrentPageDir(SB),NOSPLIT,$0
    MOVL CR3, AX
    MOVL AX, ·ret+0(FP)
    RET

TEXT ·getPageFaultAddr(SB),NOSPLIT,$0
    MOVL CR2, AX
    MOVL AX, ·ret+0(FP)
    RET

TEXT ·PAGEDIR_INDEX(SB),NOSPLIT,$0
	MOVL ·address+0(FP), AX
	SHLL $22, AX
	MOVL AX, ·ret+0(FP)
	RET

TEXT ·PAGETBL_INDEX(SB),NOSPLIT,$0
        MOVL ·address+0(FP), AX
        SHLL $12, AX
	ANDL 0x3FF, AX
        MOVL AX, ·ret+0(FP)
        RET


TEXT ·PAGEFRAME_INDEX(SB),NOSPLIT,$0
        MOVL ·address+0(FP), AX
        ANDL 0xFFF, AX
        MOVL AX, ·ret+0(FP)
        RET

TEXT ·Skupunsignedinteger32ataddress(SB),NOSPLIT,$0
        MOVL v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVL AX, 0(BX)
        RET

TEXT ·Skupbyteataddress(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·Skupunsignedinteger8ataddress(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·Osvežicr3(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, CR3
        MOVL AX, ret+0(FP)
        RET

TEXT ·getcr2(SB),NOSPLIT,$0
        MOVL CR2, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·getcr3(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·skupcr3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET

TEXT ·Getcr0(SB),NOSPLIT,$0
        MOVL CR0, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·Getcr4(SB),NOSPLIT,$0
        MOVL CR4, AX
        MOVL AX, ret+0(FP)
        RET
TEXT ·Uključenopaging(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000000, AX
    MOVL AX, CR0
    RET

