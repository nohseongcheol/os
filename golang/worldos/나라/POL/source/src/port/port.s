#include "textflag.h"

TEXT ·PortWychodzącybyte(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX //16bit
	MOVB data+2(FP), AX // 8bit
	BYTE $0xee; // out dx, al
	RET

TEXT ·PortWchodzącybyte(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX // portnumber // 16bit
	BYTE $0xec; 					// in (%dx), %al
	MOVB AL, ret+4(FP)
	RET

TEXT ·PortWychodzącysłowo(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX
	MOVW data+2(FP), AX 
	BYTE $0x66; BYTE $0xef;	// out dx, ax
	RET

TEXT ·PortWchodzącysłowo(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX
	BYTE $0x66; BYTE $0xed;	// in ax, dx
	MOVW AX, ret+4(FP)
	RET

TEXT ·PortWychodzącydword(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX
	MOVL data+4(FP), AX 
	BYTE $0xef;	// out dx, eax
	RET

TEXT ·PortWchodzącydword(SB),NOSPLIT,$0
	MOVW portnumber+0(FP), DX
	BYTE $0xed;	// in eax, dx
	MOVL AX, ret+4(FP)
	RET

