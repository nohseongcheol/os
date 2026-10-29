ENTRY(_start)
PHDRS {
    text PT_LOAD FLAGS(5);
    data PT_LOAD FLAGS(6);
    note PT_NOTE FLAGS(4);
}
SECTIONS {
    . = 0x02000000;
    .text : { KEEP(*(.text.start)) *(.text .text.*) } :text
    .rodata : { *(.rodata .rodata.*) } :text
    .note.jkoros : ALIGN(4) { KEEP(*(.note.jkoros)) } :text :note
    . = ALIGN(4096);
    .data : { *(.data .data.*) } :data
    .init_array : ALIGN(8) {
        __init_array_start = .;
        KEEP(*(SORT_BY_INIT_PRIORITY(.init_array.*))) KEEP(*(.init_array))
        __init_array_end = .;
    } :data
    .fini_array : ALIGN(8) {
        __fini_array_start = .;
        KEEP(*(SORT_BY_INIT_PRIORITY(.fini_array.*))) KEEP(*(.fini_array))
        __fini_array_end = .;
    } :data
    .bss (NOLOAD) : ALIGN(16) { *(.bss .bss.*) *(COMMON) } :data
    ASSERT(. <= 0x02c00000, "user ELF exceeds image region")
    /DISCARD/ : { *(.comment) *(.eh_frame*) *(.note.GNU-stack) }
}
