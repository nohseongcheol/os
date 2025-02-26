//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"

TEXT ·바이트출력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX //16bit
	MOVB 자료+2(FP), AX // 8bit
	BYTE $0xee; // out dx, al
	RET

TEXT ·바이트입력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX // 입출력단자번호 // 16bit
	BYTE $0xec; 					// in (%dx), %al
	MOVB AL, ret+4(FP)
	RET

TEXT ·워드출력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX
	MOVW 자료+2(FP), AX 
	BYTE $0x66; BYTE $0xef;	// out dx, ax
	RET

TEXT ·워드입력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX
	BYTE $0x66; BYTE $0xed;	// in ax, dx
	MOVW AX, ret+4(FP)
	RET

TEXT ·두배워드출력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX
	MOVL 자료+4(FP), AX 
	BYTE $0xef;	// out dx, eax
	RET

TEXT ·두배워드입력단자(SB),NOSPLIT,$0
	MOVW 입출력단자번호+0(FP), DX
	BYTE $0xed;	// in eax, dx
	MOVL AX, ret+4(FP)
	RET

