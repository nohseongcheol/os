OUTPUT_FORMAT(elf32-i386)
ENTRY(_start)
SECTIONS {
    . = 0x04000000;
    .text : { *(.text*) }
    .rodata ALIGN(4096) : { *(.rodata*) }
    .data ALIGN(4096) : { *(.data*) }
    .bss ALIGN(4096) : { *(COMMON) *(.bss*) }
    ASSERT(. < 0x04200000, "user image exceeds 2 MiB")
    /DISCARD/ : { *(.comment) *(.eh_frame) *(.note*) }
}
