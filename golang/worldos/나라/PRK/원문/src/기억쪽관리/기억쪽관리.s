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
    MOVL AX, ·반환값+0(FP)
    RET

TEXT ·getPageFaultAddr(SB),NOSPLIT,$0
    MOVL CR2, AX
    MOVL AX, ·반환값+0(FP)
    RET

TEXT ·PAGEDIR_INDEX(SB),NOSPLIT,$0
	MOVL ·주소+0(FP), AX
	SHLL $22, AX
	MOVL AX, ·반환값+0(FP)
	RET

TEXT ·PAGETBL_INDEX(SB),NOSPLIT,$0
        MOVL ·주소+0(FP), AX
        SHLL $12, AX
	ANDL 0x3FF, AX
        MOVL AX, ·반환값+0(FP)
        RET


TEXT ·PAGEFRAME_INDEX(SB),NOSPLIT,$0
        MOVL ·주소+0(FP), AX
        ANDL 0xFFF, AX
        MOVL AX, ·반환값+0(FP)
        RET

TEXT ·F주소에32비트값쓰기(SB),NOSPLIT,$0
        MOVL v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVL AX, 0(BX)
        RET

TEXT ·F주소에바이트쓰기(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·F주소에8비트값쓰기(SB),NOSPLIT,$0
        MOVB v+0(FP), AX
        MOVL addr+4(FP), BX
        MOVB AX, 0(BX)
        RET

TEXT ·F주소변환캐시갱신(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, CR3
        MOVL AX, ret+0(FP)
        RET

TEXT ·제어저장기2읽기(SB),NOSPLIT,$0
        MOVL CR2, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·제어저장기3읽기(SB),NOSPLIT,$0
        MOVL CR3, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·제어저장기3쓰기(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET

TEXT ·F제어저장기0읽기(SB),NOSPLIT,$0
        MOVL CR0, AX
        MOVL AX, ret+0(FP)
        RET

TEXT ·F제어저장기4읽기(SB),NOSPLIT,$0
        MOVL CR4, AX
        MOVL AX, ret+0(FP)
        RET
TEXT ·F기억쪽관리활성화(SB),NOSPLIT,$0
    MOVL CR0, AX
    ORL $0x80000000, AX
    MOVL AX, CR0
    RET

