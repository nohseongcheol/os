ENTRY(_start)
SECTIONS {
    . = 0x80000;
    .text : { KEEP(*(.text.boot)) *(.text .text.*) }
    .rodata : ALIGN(16) { *(.rodata .rodata.*) }
    .data : ALIGN(16) { *(.data .data.*) }
    .bss (NOLOAD) : ALIGN(16) {
        __bss_start = .;
        *(.bss .bss.*) *(COMMON)
        . = ALIGN(16);
        __bss_end = .;
    }
    .stack (NOLOAD) : ALIGN(16) {
        __stack_bottom = .;
        . += 0x40000;
        __stack_top = .;
    }
    ASSERT(. < 0x1f00000, "native kernel overlaps boot entropy / EL0 arena")
    /DISCARD/ : { *(.comment) *(.eh_frame*) *(.note*) }
}
