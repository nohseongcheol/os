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

TEXT ·haltノチfatalexception(SB),NOSPLIT,$0
	CLI
fatal_exception_halt:
	BYTE $0xF4 // HLT
	JMP fatal_exception_halt

TEXT ·アリds(SB),NOSPLIT,$0
    MOVL ds_segment+0(FP), AX
    MOVW AX, DS
    RET

TEXT ·アリgs(SB),NOSPLIT,$0
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
	CALL ·Hトッテワリコミ(SB)	\
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
	CALL ·Hトッテワリコミ(SB)	\
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
	CALL ·Hトッテexception(SB);	\
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
	CALL ·Hトッテexception(SB);	\
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
	CALL ·Hトッテexception(SB);	\
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


TEXT ·ワリコミrequesthandler0x00(SB),NOSPLIT,$0
	interrupt_handler(0x20)	
	

TEXT ·ワリコミrequesthandler0x01(SB),NOSPLIT,$0
	MOVB $0x4B, 0xB8068; 	 // char 'K'
	interrupt_handler(0x21)
	

TEXT ·ワリコミrequesthandler0x02(SB),NOSPLIT,$0
	interrupt_handler(0x22)
	

TEXT ·ワリコミrequesthandler0x03(SB),NOSPLIT,$0
	interrupt_handler(0x23)
	

TEXT ·ワリコミrequesthandler0x04(SB),NOSPLIT,$0
	interrupt_handler(0x24)
	

TEXT ·ワリコミrequesthandler0x05(SB),NOSPLIT,$0
	interrupt_handler(0x25)
	

TEXT ·ワリコミrequesthandler0x06(SB),NOSPLIT,$0
	interrupt_handler(0x26)
	

TEXT ·ワリコミrequesthandler0x07(SB),NOSPLIT,$0
	interrupt_handler(0x27)
	

TEXT ·ワリコミrequesthandler0x08(SB),NOSPLIT,$0
	interrupt_handler(0x28)
	

TEXT ·ワリコミrequesthandler0x09(SB),NOSPLIT,$0
	interrupt_handler(0x29)
	

TEXT ·ワリコミrequesthandler0x0a(SB),NOSPLIT,$0
	interrupt_handler(0x2A)
	

TEXT ·ワリコミrequesthandler0x0b(SB),NOSPLIT,$0
	interrupt_handler(0x2B)
	

TEXT ·ワリコミrequesthandler0x0c(SB),NOSPLIT,$0
	interrupt_handler(0x2C)
	

TEXT ·ワリコミrequesthandler0x0d(SB),NOSPLIT,$0
	interrupt_handler(0x2D)
	

TEXT ·ワリコミrequesthandler0x0e(SB),NOSPLIT,$0
	// Hardware IRQ14 does not push a CPU exception error code.
	interrupt_handler(0x2E)

TEXT ·ワリコミrequesthandler0x0f(SB),NOSPLIT,$0
	interrupt_handler(0x0F)

TEXT ·ワリコミrequesthandler0x80(SB),NOSPLIT,$0
	interrupt_handler(0x80)

TEXT ·ワリコミrequesthandler0x81(SB),NOSPLIT,$0
	interrupt_handler(0x81)

TEXT ·ワリコミrequesthandler0x82(SB),NOSPLIT,$0
	interrupt_handler(0x82)


TEXT ·Lidt(SB),NOSPLIT,$0
	MOVL lidtaddr+0(FP), DX
	MOVB $0x4C, 0xB8002 // char 'L'
	BYTE $0x0F; BYTE $0x01; BYTE $0x1A; // lidt [edx]
	//BYTE $0xC6; BYTE $0x05; BYTE $0x4F; BYTE $0x00; BYTE $0x00; BYTE $0x00; BYTE $0x00;// mov byte[0x4f], 0xb8000
	RET

TEXT ·Iワリコミユウコウ(SB),NOSPLIT,$0
	STI
	RET

TEXT ·Iワリコミdeactive(SB),NOSPLIT,$0
	CLI
	RET

TEXT ·ワリコミexceptionhandler0x00(SB),NOSPLIT,$0
	interrupt_exception(0x00)	

TEXT ·ワリコミexceptionhandler0x01(SB),NOSPLIT,$0
	interrupt_exception(0x01)	

TEXT ·ワリコミexceptionhandler0x02(SB),NOSPLIT,$0
	interrupt_exception(0x02)	

TEXT ·ワリコミexceptionhandler0x03(SB),NOSPLIT,$0
	interrupt_exception(0x03)	

TEXT ·ワリコミexceptionhandler0x04(SB),NOSPLIT,$0
	interrupt_exception(0x04)	

TEXT ·ワリコミexceptionhandler0x05(SB),NOSPLIT,$0
	interrupt_exception(0x05)	

TEXT ·ワリコミexceptionhandler0x06(SB),NOSPLIT,$0
	interrupt_exception(0x06)	

TEXT ·ワリコミexceptionhandler0x07(SB),NOSPLIT,$0
	interrupt_exception(0x07)	

TEXT ·ワリコミexceptionhandler0x08(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x08)	

TEXT ·ワリコミexceptionhandler0x09(SB),NOSPLIT,$0
	interrupt_exception(0x09)	

TEXT ·ワリコミexceptionhandler0x0a(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0A)	

TEXT ·ワリコミexceptionhandler0x0b(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0B)	

TEXT ·ワリコミexceptionhandler0x0c(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0C)	

TEXT ·ワリコミexceptionhandler0x0d(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x0D)	

TEXT ·ワリコミexceptionhandler0x0e(SB),NOSPLIT,$0
	// Page faults may be recoverable (for example, copy-on-write). Route them
	// through the registered paging handler and return with IRET on success.
	interrupt_handler_errorcode(0x0E)

TEXT ·ワリコミexceptionhandler0x0f(SB),NOSPLIT,$0
	interrupt_exception(0x0F)	

TEXT ·ワリコミexceptionhandler0x10(SB),NOSPLIT,$0
	interrupt_exception(0x10)	

TEXT ·ワリコミexceptionhandler0x11(SB),NOSPLIT,$0
	interrupt_exception_errorcode(0x11)	

TEXT ·ワリコミexceptionhandler0x12(SB),NOSPLIT,$0
	interrupt_exception(0x12)	

TEXT ·ワリコミexceptionhandler0x13(SB),NOSPLIT,$0
	interrupt_exception(0x13)	

TEXT ·ワリコミignore(SB),NOSPLIT,$0
	MOVB $0x4D, 0xB8048 // char 'M'
	IRETL;

TEXT ·ワリコミシュウリョウloop(SB),NOSPLIT,$0
	STI
	BYTE $0xF4
	BYTE $0xEB; BYTE $0xFD

TEXT ·アリcr3(SB),NOSPLIT,$0
        MOVL cr3+0(FP), AX
        MOVL AX, CR3
        RET
