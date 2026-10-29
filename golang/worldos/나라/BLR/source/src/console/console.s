#include "textflag.h"
#include "go_asm.h"

// 16550-compatible COM1, 38400 baud, 8 data bits, no parity, one stop bit.
// VirtualBox exposes this UART and writes its bytes into build/virtualbox-current.log.
TEXT ·Serialinit(SB),NOSPLIT,$0
	MOVW $0x3F9, DX
	XORL AX, AX
	BYTE $0xEE // out dx, al: disable UART interrupts

	MOVW $0x3FB, DX
	MOVB $0x80, AX
	BYTE $0xEE // enable divisor latch

	MOVW $0x3F8, DX
	MOVB $0x03, AX
	BYTE $0xEE // divisor low: 115200 / 3 = 38400

	MOVW $0x3F9, DX
	XORL AX, AX
	BYTE $0xEE // divisor high

	MOVW $0x3FB, DX
	MOVB $0x03, AX
	BYTE $0xEE // 8N1

	MOVW $0x3FA, DX
	MOVB $0xC7, AX
	BYTE $0xEE // enable and clear FIFO

	MOVW $0x3FC, DX
	MOVB $0x0B, AX
	BYTE $0xEE // DTR, RTS and OUT2
	RET

// Use a bounded readiness poll. A missing/misconfigured UART must never hang
// the kernel while it is trying to report the original fault.
TEXT ·SerialЗапісbyte(SB),NOSPLIT,$0
	MOVL $65535, CX
serial_wait:
	MOVW $0x3FD, DX
	BYTE $0xEC // in al, dx: line status register
	TESTB $0x20, AX
	JNZ serial_send
	LOOP serial_wait
	RET
serial_send:
	MOVW $0x3F8, DX
	MOVB data+0(FP), AX
	BYTE $0xEE // out dx, al
	RET


TEXT ·MДрукаваць(SB),NOSPLIT,$0
	MOVL phyaddr+0(FP), AX

	MOVB data+4(FP), BX

	MOVL x+8(FP), CX
	MOVL x+12(FP), DX
	IMULL $80, DX
	IMULL $2, DX

	ADDL DX, CX

	ADDL CX, AX
        MOVB BX, 0(AX)
        RET
