#include "textflag.h"

TEXT ·이nablePaging(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000000, AX
    MOVL AX, CR0
    RET

TEXT ·에스witchPageDir(SB),NOSPLIT,$0
    MOVL ·dir+0(FP), AX
    MOVL AX, CR3
    RET

TEXT ·지etCurrentPageDir(SB),NOSPLIT,$0
    MOVL CR3, AX
    MOVL AX, ·알이티+0(FP)
    RET

TEXT ·지etPageFaultAddr(SB),NOSPLIT,$0
    MOVL CR2, AX
    MOVL AX, ·알이티+0(FP)
    RET

TEXT ·PAGEDIR_INDEX(SB),NOSPLIT,$0
	MOVL ·에이디디알+0(FP), AX
	SHLL $22, AX
	MOVL AX, ·알이티+0(FP)
	RET

TEXT ·PAGETBL_INDEX(SB),NOSPLIT,$0
        MOVL ·에이디디알+0(FP), AX
        SHLL $12, AX
	ANDL 0x3FF, AX
        MOVL AX, ·알이티+0(FP)
        RET


TEXT ·PAGEFRAME_INDEX(SB),NOSPLIT,$0
        MOVL ·에이디디알+0(FP), AX
        ANDL 0xFFF, AX
        MOVL AX, ·알이티+0(FP)
        RET

TEXT ·S셋유아이엔티32에이티에이디디알(SB),NOSPLIT,$0
        MOVL v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVL AX, 0(BX)
        RET

TEXT ·S셋바이트에이티에이디디알(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·S셋유아이엔티8에이티에이디디알(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·R알이엘오에이디시에이알3(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, CR3
        MOVL AX, ret+0(FP)
        RET

TEXT ·겟시에이알2(SB),NOSPLIT,$0
        MOVL CR2, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·겟시에이알3(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·셋시에이알3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET

TEXT ·G겟시에이알0(SB),NOSPLIT,$0
        MOVL CR0, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·G겟시에이알4(SB),NOSPLIT,$0
        MOVL CR4, AX
        MOVL AX, ret+0(FP)
        RET
TEXT ·E이엔에이비엘이페이징(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000000, AX
    MOVL AX, CR0
    RET

