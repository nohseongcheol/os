//Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved

#include "textflag.h"
#include "go_asm.h"

#define 개입중단_처리기(num) \
        PUSHL DS;               \
        PUSHL ES;               \
        \//PUSHL FS;            \
        \//PUSHL GS;            \
                                \
        PUSHL BP;               \
        PUSHL DI;               \
        PUSHL SI;               \
                                \
        PUSHL DX;               \
        PUSHL CX;               \
        PUSHL BX;               \
        PUSHL AX;               \
                                \
        PUSHL $0;               \
        PUSHL $0;               \
                                \
        MOVL $num, 4(SP);       \
        MOVL SP, 0(SP);         \
	CALL interrupt·개입중단처리(SB)	\
                                \
        MOVL AX, SP;            \
                                \
        POPL AX;                \
        POPL AX;                \
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
        \//POPL GS;             \
        \//POPL FS;             \
        POPL ES;                \
        POPL DS;                \
                                \
        IRETL;                  \
        ;

#define 개입중단예외_처리기(num) \
	PUSHL DS;		\
	PUSHL ES;		\
				\
        PUSHL BP;               \
        PUSHL DI;               \
        PUSHL SI;               \
                                \
        PUSHL DX;               \
        PUSHL CX;               \
        PUSHL BX;               \
        PUSHL AX;               \
				\
	PUSHL 0;		\
	PUSHL 0;		\
				\
        MOVL $num, 4(SP);		\
        MOVL SP, 0(SP);		\
	CALL interrupt·예외처리(SB)	\
                                \
	MOVL AX, SP;		\
				\
        POPL AX;                \
        POPL AX;                \
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
        POPL ES;                \
        POPL DS;                \
				\
	IRETL;			\
        ;

TEXT ·개입중단_요청처리0x00(SB),NOSPLIT,$0
	개입중단_처리기(0x20)	
	

TEXT ·개입중단_요청처리0x01(SB),NOSPLIT,$0
	개입중단_처리기(0x21)
	

TEXT ·개입중단_요청처리0x02(SB),NOSPLIT,$0
	개입중단_처리기(0x22)
	

TEXT ·개입중단_요청처리0x03(SB),NOSPLIT,$0
	개입중단_처리기(0x23)
	

TEXT ·개입중단_요청처리0x04(SB),NOSPLIT,$0
	개입중단_처리기(0x24)
	

TEXT ·개입중단_요청처리0x05(SB),NOSPLIT,$0
	개입중단_처리기(0x25)
	

TEXT ·개입중단_요청처리0x06(SB),NOSPLIT,$0
	개입중단_처리기(0x26)
	

TEXT ·개입중단_요청처리0x07(SB),NOSPLIT,$0
	개입중단_처리기(0x27)
	

TEXT ·개입중단_요청처리0x08(SB),NOSPLIT,$0
	개입중단_처리기(0x28)
	

TEXT ·개입중단_요청처리0x09(SB),NOSPLIT,$0
	개입중단_처리기(0x29)
	

TEXT ·개입중단_요청처리0x0A(SB),NOSPLIT,$0
	개입중단_처리기(0x2A)
	

TEXT ·개입중단_요청처리0x0B(SB),NOSPLIT,$0
	개입중단_처리기(0x2B)
	

TEXT ·개입중단_요청처리0x0C(SB),NOSPLIT,$0
	개입중단_처리기(0x2C)
	

TEXT ·개입중단_요청처리0x0D(SB),NOSPLIT,$0
	개입중단_처리기(0x2D)
	

TEXT ·개입중단_요청처리0x0E(SB),NOSPLIT,$0
	개입중단_처리기(0x2E)
	

TEXT ·개입중단_요청처리0x0F(SB),NOSPLIT,$0
	개입중단_처리기(0x2F)


TEXT ·개입중단_요청처리0x80(SB),NOSPLIT,$0
	개입중단_처리기(0x80)


TEXT ·개입중단서술자표_적재(SB),NOSPLIT,$0
	MOVL lidtaddr+0(FP), DX
	BYTE $0x0F; BYTE $0x01; BYTE $0x1A; // lidt [edx]
	RET

TEXT ·개입중단활성화(SB),NOSPLIT,$0
	STI
	RET

TEXT ·개입중단비활성화(SB),NOSPLIT,$0
	CLI
	RET

TEXT ·개입중단_예외처리0x00(SB),NOSPLIT,$0
	개입중단예외_처리기(0x00)	

TEXT ·개입중단_예외처리0x01(SB),NOSPLIT,$0
	개입중단예외_처리기(0x01)	

TEXT ·개입중단_예외처리0x02(SB),NOSPLIT,$0
	개입중단예외_처리기(0x02)	

TEXT ·개입중단_예외처리0x03(SB),NOSPLIT,$0
	개입중단예외_처리기(0x03)	

TEXT ·개입중단_예외처리0x04(SB),NOSPLIT,$0
	개입중단예외_처리기(0x04)	

TEXT ·개입중단_예외처리0x05(SB),NOSPLIT,$0
	개입중단예외_처리기(0x05)	

TEXT ·개입중단_예외처리0x06(SB),NOSPLIT,$0
	개입중단예외_처리기(0x06)	

TEXT ·개입중단_예외처리0x07(SB),NOSPLIT,$0
	개입중단예외_처리기(0x07)	

TEXT ·개입중단_예외처리0x08(SB),NOSPLIT,$0
	개입중단예외_처리기(0x08)	

TEXT ·개입중단_예외처리0x09(SB),NOSPLIT,$0
	개입중단예외_처리기(0x09)	

TEXT ·개입중단_예외처리0x0A(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0A)	

TEXT ·개입중단_예외처리0x0B(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0B)	

TEXT ·개입중단_예외처리0x0C(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0C)	

TEXT ·개입중단_예외처리0x0D(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0D)	

TEXT ·개입중단_예외처리0x0E(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0E)	

TEXT ·개입중단_예외처리0x0F(SB),NOSPLIT,$0
	개입중단예외_처리기(0x0F)	

TEXT ·개입중단_무시하기(SB),NOSPLIT,$0
	IRETL;
