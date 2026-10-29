LD := ld
AS := ~/nasm/nasm-2.15.05/nasm
LD_FLAGS := -n -melf_i386 -T linker.ld -static --no-ld-generated-unwind-info
#LD_FLAGS := -n -T linker.ld -static --no-ld-generated-unwind-info

ASM_FILES := src/asm/multiboot_header.s src/asm/rt0.s
OBJ_FILES := build/multiboot_header.o build/rt0.o build/go.o

.PHONY: current current-iso current-qemu

CURRENT_TEST_DISK ?= /home/user/VirtualBox VMs/eng operating system/NewVirtualDisk1-fixed-20260908.vdi

# engos 현행 기능을 한글 독음 식별자로 옮긴 독립 구현.
current:
	$(MAKE) -C 현행 kernel

current-iso:
	$(MAKE) -C 현행 iso

current-qemu: current-iso
	qemu-system-x86_64 -boot d \
		-drive 'file=현행/build/kernel.iso,media=cdrom,if=none,id=cd0' \
		-device ide-cd,drive=cd0,bus=ide.1,unit=0 \
		-drive 'file=$(CURRENT_TEST_DISK),format=vdi,if=none,id=disk0,snapshot=on' \
		-device ide-hd,drive=disk0,bus=ide.0,unit=1 \
		-m 512 -serial stdio
#OBJ_FILES := build/multiboot_header.o build/go.o

defult: mkdir $(OBJ_FILES)

mkdir:
	-mkdir -p build

#build/boot.o: boot.asm
	#$(AS) -g -f elf32 -F dwarf -o $@ $<
build/multiboot_header.o: asm/multiboot_header.s
	$(AS) -g -f elf32 -F dwarf -o $@ $<
build/rt0.o: asm/rt0.s
	$(AS) -g -f elf32 -F dwarf -I asm/ -o $@ $<
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
	VirtualBox --startvm "kor operating system" --debug &
	
