OUTPUT_FORMAT(elf32-i386)
OUTPUT_ARCH(i386:i386)

LOAD_ADDRESS = 0x400000;
PAGE_OFFSET = 0;
/* PAGE_OFFSET = 0xC0000000; */
VMA = PAGE_OFFSET + LOAD_ADDRESS;

ENTRY(_rt0_entry)
/* ENTRY(_rt0_32_entry) */

SECTIONS {
	/* Kernel starts at 1M */
	. = VMA;

	/* ensure that the multiboot header is at the beginning */	
	/*
	.multiboot :
	{
	}
	*/

	.text ALIGN(4K) : AT(ADDR(.text) - PAGE_OFFSET)
	{
		*(.multiboot_header)
		*(.text)
	}

	/* Read-only data. */
	.rodata ALIGN(4K) : AT(ADDR(.rodata) - PAGE_OFFSET)
	{
		*(.rodata)
	}

	/* Read-write data (initialized) */
	.data ALIGN(4K) :  AT(ADDR(.data) - PAGE_OFFSET)
	{
		*(.data)
	}

	.bss ALIGN(4K) :  AT(ADDR(.bss) - PAGE_OFFSET) 
	{
		*(COMMON)
		*(.bss)
	}

}
