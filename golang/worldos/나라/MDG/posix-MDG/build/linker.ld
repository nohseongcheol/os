LOAD_ADDRESS = 0x5000000;
/* PAGE_OFFSET = 0x80; */
PAGE_OFFSET = 0x00;
VMA = PAGE_OFFSET + LOAD_ADDRESS;

ENTRY(main)

SECTIONS {
	/* Kernel starts at 1M */
	. = VMA;

	.text :
	{
		*(.text)
	}

	/* Read-only data. */
	.rodata :
	{
		*(.rodata)
	}

	/* Read-write data (initialized) */
	.data :
	{
		*(.data)
	}

	.bss :
	{
		*(.bss)
	}

}
