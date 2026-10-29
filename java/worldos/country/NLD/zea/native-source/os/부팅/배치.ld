OUTPUT_FORMAT(elf32-i386)
ENTRY(_start)
SECTIONS {
    . = 1M;
    .multiboot : { KEEP(*(.multiboot)) }
    .text ALIGN(4096) : { *(.text*) }
    .rodata ALIGN(4096) : { *(.rodata*) }
    .data ALIGN(4096) : { *(.data*) }
    .bss ALIGN(4096) : {
        bss_start = .;
        *(COMMON) *(.bss*)
        bss_end = .;
    }
    ASSERT(. < 0x00800000, "kernel overlaps private user physical memory")
    /DISCARD/ : { *(.comment) *(.eh_frame) *(.note*) }
}
