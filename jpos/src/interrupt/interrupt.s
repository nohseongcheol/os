//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"
#include "go_asm.h"

#define 割り込み_処理器(num) \
        PUSHL BP;               \
        PUSHL DI;               \
        PUSHL SI;               \
                                \
        PUSHL DX;               \
        PUSHL CX;               \
        PUSHL BX;               \
        PUSHL AX;               \
				\
				\	
        MOVB $num, 4(SP);	\
        MOVL SP, 0(SP);		\
	CALL interrupt·割り込み処理(SB)	\
                                \
	MOVL AX, SP;		\
				\
        POPL AX;                \
        POPL BX;                \
        POPL CX;                \
        POPL DX;                \
                                \
        POPL SI;                \
        POPL DI;                \
        POPL BP;                \
				\
				\
	IRETL;			\
        ;

#define 割り込み例外_処理機(num) \
        PUSHL BP;               \
        PUSHL DI;               \
        PUSHL SI;               \
                                \
        PUSHL DX;               \
        PUSHL CX;               \
        PUSHL BX;               \
        PUSHL AX;               \
				\
        MOVB $num, 4(SP);		\
        MOVL SP, 0(SP);		\
	CALL interrupt·例外処理(SB)	\
                                \
	MOVL AX, SP;		\
				\
        POPL AX;                \
        POPL BX;                \
        POPL CX;                \
        POPL DX;                \
                                \
        POPL SI;                \
        POPL DI;                \
        POPL BP;                \
				\
	IRETL;			\
        ;

TEXT ·割り込み_要請処理0x00(SB),NOSPLIT,$0
	割り込み_処理器(0x20)	
	

TEXT ·割り込み_要請処理0x01(SB),NOSPLIT,$0
	割り込み_処理器(0x21)
	

TEXT ·割り込み_要請処理0x02(SB),NOSPLIT,$0
	割り込み_処理器(0x22)
	

TEXT ·割り込み_要請処理0x03(SB),NOSPLIT,$0
	割り込み_処理器(0x23)
	

TEXT ·割り込み_要請処理0x04(SB),NOSPLIT,$0
	割り込み_処理器(0x24)
	

TEXT ·割り込み_要請処理0x05(SB),NOSPLIT,$0
	割り込み_処理器(0x25)
	

TEXT ·割り込み_要請処理0x06(SB),NOSPLIT,$0
	割り込み_処理器(0x26)
	

TEXT ·割り込み_要請処理0x07(SB),NOSPLIT,$0
	割り込み_処理器(0x27)
	

TEXT ·割り込み_要請処理0x08(SB),NOSPLIT,$0
	割り込み_処理器(0x28)
	

TEXT ·割り込み_要請処理0x09(SB),NOSPLIT,$0
	割り込み_処理器(0x29)
	

TEXT ·割り込み_要請処理0x0A(SB),NOSPLIT,$0
	割り込み_処理器(0x2A)
	

TEXT ·割り込み_要請処理0x0B(SB),NOSPLIT,$0
	割り込み_処理器(0x2B)
	

TEXT ·割り込み_要請処理0x0C(SB),NOSPLIT,$0
	割り込み_処理器(0x2C)
	

TEXT ·割り込み_要請処理0x0D(SB),NOSPLIT,$0
	割り込み_処理器(0x2D)
	

TEXT ·割り込み_要請処理0x0E(SB),NOSPLIT,$0
	割り込み_処理器(0x2E)
	

TEXT ·割り込み_要請処理0x0F(SB),NOSPLIT,$0
	割り込み_処理器(0x2F)


TEXT ·割り込み記述子表を搭載(SB),NOSPLIT,$0
	MOVL lidtaddr+0(FP), DX
	BYTE $0x0F; BYTE $0x01; BYTE $0x1A; // lidt [edx]
	RET

TEXT ·割り込み活性化(SB),NOSPLIT,$0
	STI
	RET

TEXT ·割り込み非活性化(SB),NOSPLIT,$0
	CLI
	RET

TEXT ·割り込み_例外処理0x00(SB),NOSPLIT,$0
	割り込み例外_処理機(0x00)	

TEXT ·割り込み_例外処理0x01(SB),NOSPLIT,$0
	割り込み例外_処理機(0x01)	

TEXT ·割り込み_例外処理0x02(SB),NOSPLIT,$0
	割り込み例外_処理機(0x02)	

TEXT ·割り込み_例外処理0x03(SB),NOSPLIT,$0
	割り込み例外_処理機(0x03)	

TEXT ·割り込み_例外処理0x04(SB),NOSPLIT,$0
	割り込み例外_処理機(0x04)	

TEXT ·割り込み_例外処理0x05(SB),NOSPLIT,$0
	割り込み例外_処理機(0x05)	

TEXT ·割り込み_例外処理0x06(SB),NOSPLIT,$0
	割り込み例外_処理機(0x06)	

TEXT ·割り込み_例外処理0x07(SB),NOSPLIT,$0
	割り込み例外_処理機(0x07)	

TEXT ·割り込み_例外処理0x08(SB),NOSPLIT,$0
	割り込み例外_処理機(0x08)	

TEXT ·割り込み_例外処理0x09(SB),NOSPLIT,$0
	割り込み例外_処理機(0x09)	

TEXT ·割り込み_例外処理0x0A(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0A)	

TEXT ·割り込み_例外処理0x0B(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0B)	

TEXT ·割り込み_例外処理0x0C(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0C)	

TEXT ·割り込み_例外処理0x0D(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0D)	

TEXT ·割り込み_例外処理0x0E(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0E)	

TEXT ·割り込み_例外処理0x0F(SB),NOSPLIT,$0
	割り込み例外_処理機(0x0F)	

TEXT ·割り込み_無視する(SB),NOSPLIT,$0
	IRETL;
