//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"
#include "go_asm.h"

TEXT ·공용서술자표_올리기(SB),NOSPLIT,$0
	MOVL x+0(FP), DX
	//MOVB $0x4F, 0xB8030 //char o
	//MOVB DH, 0xB8034
	//MOVB DL, 0xB8036
	//MOVW DX, 0xB8038

	//BYTE $0x0f; BYTE $0x00; BYTE $0x12; // lldt [edx]
	//CLI
	BYTE $0x0f; BYTE $0x01; BYTE $0x12; // lgdt [edx]
	//MOVL AX, 0xB8000
	// mov dword [0xb8000], 0x4F
	//BYTE $0xC7; BYTE $0x05; BYTE $0x00; BYTE $0x80; BYTE $0x0B; BYTE $0x00; BYTE $0x41; BYTE $0x00; BYTE $0x00; BYTE $0x00;
	// mov dword [0xb8000], eax
	//BYTE $0xA3; BYTE $0x00; BYTE $0x80; BYTE $0x0B; BYTE $0x00;
	//MOVB $0x4F, 0xB8032 //char o

	//BYTE $0xb8; BYTE $0x18; BYTE $0x00; // mov  ax, 0x18
	//BYTE $0x8e; BYTE $0xd8; // mov  ds, ax
	//BYTE $0x8e; BYTE $0xe8; // mov  gs, ax
	//BYTE $0x8e; BYTE $0xe0; // mov  fs, ax
	//BYTE $0x8e; BYTE $0xe0; // mov  es, ax

	//MOVL (DS), ($0x18)
	//MOVL $0x10, (CS)
	//MOVL $0x18, (DS)
	//MOVL $0x18, (ES)
	//MOVL $0x18, (FS)
	//MOVL $0x18, (GS)
	//MOVL $0x18, (SS)
	
        RET

