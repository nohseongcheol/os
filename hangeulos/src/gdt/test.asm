[bits 32]
reloadSegments:
	JMP 0x10:reload_CS
reload_CS:
	mov ax, 0x10
	RET
