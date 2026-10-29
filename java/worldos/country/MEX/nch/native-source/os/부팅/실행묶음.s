.section .rodata.apps,"a"
.balign 16
.globl app_blob_start, app_blob_end
app_blob_start:
.incbin "build/apps.bin"
app_blob_end:
.section .note.GNU-stack,"",@progbits
