#include "textflag.h"
#include "go_asm.h"

#define KERNEL_DATA_SELECTOR 0x10
#define KERNEL_GS_SELECTOR 0x18
#define USER_DATA_SELECTOR 0x2B
#define USER_GS_SELECTOR 0x33

GLOBL ·exceptionStack<>(SB), NOPTR, $4096

TEXT ·exceptioncr0(SB),NOSPLIT,$0
	MOVL CR0, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·exceptioncr2(SB),NOSPLIT,$0
	MOVL CR2, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·exceptioncr3(SB),NOSPLIT,$0
	MOVL CR3, AX
	MOVL AX, ret+0(FP)
	RET

TEXT ·haltСледfatalexception(SB),NOSPLIT,$0
	CLI
fatal_exception_halt:
	BYTE $0xF4 // HLT
	JMP fatal_exception_halt

TEXT ·задайds(SB),NOSPLIT,$0
    MOVL ds_segment+0(FP), AX
    MOVW AX, DS
    RET

TEXT ·задайgs(SB),NOSPLIT,$0
    MOVL gs_segment+0(FP), AX
    MOVW AX, GS
    RET

#define interrupt_handler(num) \
	CLI;			\
	PUSHL DS;		\
	PUSHL ES;		\
	PUSHL FS;		\
	PUSHL GS;		\
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
	MOVL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
				\
	/* p1/p2 are part of TCPUState; keep Go call arguments separate. */ \
	PUSHL $0;		\
	PUSHL $0;		\
	MOVL SP, BX;		\
	SUBL $12, SP;		\
	MOVL BX, 0(SP);		\
	MOVL $num, 4(SP);	\
	MOVL $0, 8(SP);	\
	CALL ·РъкохваткаПрекъсване(SB)	\
	MOVL 8(SP), AX;	\
	ADDL $12, SP;		\
	MOVL AX, SP;		\
				\
        POPL AX;                \
        POPL AX;                \
				\
	MOVL 48(SP), AX;	\
	ANDL $3, AX;		\
	IMULL $9, AX;		\
	MOVL AX, CX;		\
	ADDL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL CX, AX;		\
	ADDL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
				\
        POPL AX;                \
        POPL BX;                \
        POPL CX;                \
        POPL DX;                \
                                \
				\
        POPL SI;                \
        POPL DI;                \
        POPL BP;                \
				\
	ADDL $16, SP;		\
				\
	ORL $0x200, 8(SP);	\
	IRETL;			\
				\

#define interrupt_handler_errorcode(num) \
	CLI;			\
	PUSHL DS;		\
	PUSHL ES;		\
	PUSHL FS;		\
	PUSHL GS;		\
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
	MOVL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
				\
	/* p1/p2 are part of TCPUState; keep Go call arguments separate. */ \
	PUSHL $0;		\
	PUSHL $0;		\
	MOVL SP, BX;		\
	SUBL $12, SP;		\
	MOVL BX, 0(SP);		\
	MOVL $num, 4(SP);	\
	MOVL $0, 8(SP);	\
	CALL ·РъкохваткаПрекъсване(SB)	\
	MOVL 8(SP), AX;	\
	ADDL $12, SP;		\
	MOVL AX, SP;		\
				\
        POPL AX;                \
        POPL AX;                \
				\
	MOVL 52(SP), AX;	\
	ANDL $3, AX;		\
	IMULL $9, AX;		\
	MOVL AX, CX;		\
	ADDL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL CX, AX;		\
	ADDL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
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
	ADDL $16, SP;		\
				\
	ADDL $4, SP;		\
	ORL $0x200, 8(SP);	\
	IRETL;			\
				\

#define interrupt_exception(num) \
	CLI;			\
	MOVB $0x4D, 0xB8070; 	 \// char 'M'
	MOVL SP, BX;		\
	MOVL $·exceptionStack<>+4096(SB), SP;	\
	MOVL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
	PUSHL $0;		\
	PUSHL $0;		\
        MOVB $num, 4(SP);	\
        MOVL BX, 0(SP);		\
	CALL ·Ръкохваткаexception(SB);	\
	BYTE $0xF4;		\
	BYTE $0xEB; BYTE $0xFD;	\
	;

#define interrupt_exception_errorcode(num) \
	CLI;			\
	MOVB $0x4D, 0xB8070; 	 \// char 'M'
	MOVL SP, BX;		\
	MOVL $·exceptionStack<>+4096(SB), SP;	\
	MOVL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
	PUSHL $0;		\
	PUSHL $0;		\
        MOVB $num, 4(SP);	\
        MOVL BX, 0(SP);		\
	CALL ·Ръкохваткаexception(SB);	\
	BYTE $0xF4;		\
	BYTE $0xEB; BYTE $0xFD;	\
	;

#define interrupt_exception_resume(num) \
	CLI;			\
	MOVL SP, BX;		\
	PUSHL DS;		\
	PUSHL ES;		\
	PUSHL FS;		\
	PUSHL GS;		\
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
	MOVL $KERNEL_DATA_SELECTOR, AX;	\
	MOVW AX, DS;		\
	MOVW AX, ES;		\
	MOVW AX, FS;		\
	MOVL $KERNEL_GS_SELECTOR, AX;	\
	MOVW AX, GS;		\
				\
	PUSHL $0;		\
	PUSHL $0;		\
        MOVB $num, 4(SP);	\
        MOVL BX, 0(SP);		\
	CALL ·Ръкохваткаexception(SB);	\
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
	POPL GS;		\
	POPL FS;		\
	POPL ES;		\
	POPL DS;		\
				\
	IRETL;			\
	;


TEXT ·прекъсванеrequesthandler0x00(SB),NOSPLIT,$0
	interrupt_handler(0x20)	
	

TEXT ·прекъсванеrequesthandler0x01(SB),NOSPLIT,$0
	MOVB $0x4B, 0xB8068; 	 // char 'K'
	interrupt_handler(0x21)
	

TEXT ·прекъсванеrequesthandler0x02(SB),NOSPLIT,$0
	interrupt_handler(0x22)
	

TEXT ·прекъсванеrequesthandler0x03(SB),NOSPLIT,$0
	interrupt_handler(0x23)
	

TEXT ·прекъсванеrequesthandler0x04(SB),NOSPLIT,$0
	interrupt_handler(0x24)
	

TEXT ·прекъсванеrequesthandler0x05(SB),NOSPLIT,$0
	interrupt_handler(0x25)
	

TEXT ·прекъсванеrequesthandler0x06(SB),NOSPLIT,$0
	interrupt_handler(0x26)
	

TEXT ·прекъсванеrequesthandler0x07(SB),NOSPLIT,$0
	interrupt_handler(0x27)
	

TEXT ·прекъсванеrequesthandler0x08(SB),NOSPLIT,$0
	interrupt_handler(0x28)
	

TEXT ·прекъсванеrequesthandler0x09(SB),NOSPLIT,$0
	interrupt_handler(0x29)
	

TEXT ·прекъсванеrequesthandler0x0a(SB),NOSPLIT,$0
	interrupt_handler(0x2A)
	

TEXT ·прекъсванеrequesthandler0x0b(SB),NOSPLIT,$0
	interrupt_handler(0x2B)
	

TEXT ·прекъсванеrequesthandler0x0c(SB),NOSPLIT,$0
	interrupt_handler(0x2C)
	

TEXT ·прекъсванеrequesthandler0x0d(SB),NOSPLIT,$0
	interrupt_handler(0x2D)
	

TEXT ·прекъсванеrequesthandler0x0e(SB),NOSPLIT,$0
	// Hardware IRQ14 does not push a CPU exception error code.
	interrupt_handler(0x2E)

TEXT ·прекъсванеrequesthandler0x0f(SB),NOSPLIT,$0
	interrupt_handler(0x0F)

TEXT ·прекъсванеrequesthandler0x80(SB),NOSPLIT,$0
	interrupt_handler(0x80)

TEXT ·прекъсванеrequesthandler0x81(SB),NOSPLIT,$0
	interrupt_handler(0x81)

TEXT ·прекъсванеrequesthandler0x82(SB),NOSPLIT,$0
	interrupt_handler(0x82)


TEXT ·Lidt(SB),NOSPLIT,$0
	MOVL lidtaddr+0(FP), DX
	MOVB $0x4C, 0xB8002 // char 'L'
	BYTE $0x0F; BYTE $0x01; BYTE $0x1A; // lidt [edx]
	//BYTE $0xC6; BYTE $0x05; BYTE $0x4F; BYTE $0x00; BYTE $0x00; BYTE $0x00; BYTE $0x00;// mov byte[0x4f], 0xb8000
	RET

TEXT ·ПрекъсванеАктивна(SB),NOSPLIT,$0
	STI
	RET

TEXT ·Прекъсванеdeactive(SB),NOSPLIT,$0
	CLI
	RET

TEXT ·прекъсванеexceptionhandler0x00(SB),NOSPLIT,$0
	interrupt_exception(0x00)	

TEXT ·прекъсванеexceptionhandler0x01(SB),NOSPLIT,$0
	interrupt_exception(0x01)	

TEXT ·прекъсванеexceptionhandler0x02(SB),NOSPLIT,$0
	interrupt_exception(0x02)	

TEXT ·прекъсванеexceptionhandler0x03(SB),NOSPLIT,$0
	interrupt_exception(0x03)	

TEXT ·прекъсванеexceptionhandler0x04(SB),NOSPLIT,$0
	interrupt_exception(0x04)	

TEXT ·прекъсванеexceptionhandler0x05(SB),NOSPLIT,$0
	interrupt_exception(0x05)	

TEXT ·прекъсванеexceptionhandler0x06(SB),NOSPLIT,$0
	interrupt_exception(0x06)	

TEXT ·прекъсванеexceptionhandler0x07(SB),NOSPLIT,$0
	interrupt_exception(0x07)	

TEXT ·прекъсванеexceptionhandler0x08(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x08)	

TEXT ·прекъсванеexceptionhandler0x09(SB),NOSPLIT,$0
	interrupt_exception(0x09)	

TEXT ·прекъсванеexceptionhandler0x0a(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0A)	

TEXT ·прекъсванеexceptionhandler0x0b(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0B)	

TEXT ·прекъсванеexceptionhandler0x0c(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0C)	

TEXT ·прекъсванеexceptionhandler0x0d(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0D)	

TEXT ·прекъсванеexceptionhandler0x0e(SB),NOSPLIT,$0
	// Page faults may be recoverable (for example, copy-on-write). Route them
	// through the registered paging handler and return with IRET on success.
	interrupt_handler_errorcode(0x0E)

TEXT ·прекъсванеexceptionhandler0x0f(SB),NOSPLIT,$0
	interrupt_exception(0x0F)	

TEXT ·прекъсванеexceptionhandler0x10(SB),NOSPLIT,$0
	interrupt_exception(0x10)	

TEXT ·прекъсванеexceptionhandler0x11(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x11)	

TEXT ·прекъсванеexceptionhandler0x12(SB),NOSPLIT,$0
	interrupt_exception(0x12)	

TEXT ·прекъсванеexceptionhandler0x13(SB),NOSPLIT,$0
	interrupt_exception(0x13)	

TEXT ·прекъсванеignore(SB),NOSPLIT,$0
	MOVB $0x4D, 0xB8048 // char 'M'
	IRETL;

TEXT ·прекъсванеИзходloop(SB),NOSPLIT,$0
	STI
	BYTE $0xF4
	BYTE $0xEB; BYTE $0xFD

TEXT ·задайcr3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET
