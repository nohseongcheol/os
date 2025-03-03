LD := ld
LD_FLAGS := -n -melf_i386 -T linker.ld -static --no-ld-generated-unwind-info
#LD_FLAGS := -n -T linker.ld -static --no-ld-generated-unwind-info

ASM_FILES := src/asm/multiboot_header.s src/asm/rt0.s
OBJ_FILES := build/multiboot_header.o build/rt0.o build/go.o
#OBJ_FILES := build/multiboot_header.o build/go.o

defult: mkdir $(OBJ_FILES)

mkdir:
	-mkdir -p build

#build/boot.o: boot.asm
	#nasm -g -f elf32 -F dwarf -o $@ $<
build/multiboot_header.o: asm/multiboot_header.s
	nasm -g -f elf32 -F dwarf -o $@ $<
build/rt0.o: asm/rt0.s
	nasm -g -f elf32 -F dwarf -I asm/ -o $@ $<
build/go.o: 
	@bash go.sh | sh
	@objcopy \
                --globalize-symbol runtime.g0 \
                --globalize-symbol main.main \
                --globalize-symbol main.kmain \
                --globalize-symbol gdt.Init \
                 build/go.o build/go.o

build/kernel.bin: $(OBJ_FILES)
	@echo "[$(LD)] linking kernel.bin"
	$(LD) $(LD_FLAGS) -o $@ $(OBJ_FILES)
kernel:build/kernel.bin

clean:
	rm -rf build

qemu: build/kernel.bin
	qemu-system-i386 -kernel $<

iso: build/kernel.bin
	mkdir iso
	mkdir iso/boot
	mkdir iso/boot/grub
	cp $< iso/boot/
	echo 'set timeout=0' >> iso/boot/grub/grub.cfg
	echo 'set default=0' >> iso/boot/grub/grub.cfg
	echo '' >> iso/boot/grub/grub.cfg
	echo 'menuentry "eng operating system" {' >> iso/boot/grub/grub.cfg
	echo 'multiboot2 /boot/kernel.bin' >> iso/boot/grub/grub.cfg
	echo 'boot' >> iso/boot/grub/grub.cfg
	echo '}' >> iso/boot/grub/grub.cfg
	grub-mkrescue --output=build/kernel.iso iso
	rm -rf iso
vbox:iso
	(killall VirtualBox) || true
	VirtualBox --startvm "jp operating system" --debug &
	
