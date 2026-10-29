NASM ?= nasm
LD := ld
LD_FLAGS := -n -melf_i386 -T link_layout.ld -static --no-ld-generated-unwind-info
#LD_FLAGS := -n -T link_layout.ld -static --no-ld-generated-unwind-info

ASM_FILES := src/machine_boot/multibootheader.s src/machine_boot/rt0.s
OBJ_FILES := build/multiboot_header.o build/rt0.o build/go.o
#OBJ_FILES := build/multiboot_header.o build/go.o

VM_NAME ?= worldos FLK
VBOX_LOG := $(abspath build/virtualbox-current.log)

.PHONY: default clean kernel qemu iso vbox vbox-config vbox-log diagnose

default: kernel

build:
	mkdir -p build

build/multiboot_header.o: machine_boot/multibootheader.s | build
	$(NASM) -g -f elf32 -F dwarf -o $@ $<
build/rt0.o: machine_boot/rt0.s | build
	$(NASM) -g -f elf32 -F dwarf -I machine_boot/ -o $@ $<
build/go.o: | build
	@bash compile_kernel.sh | sh

build/kernel.bin: $(OBJ_FILES)
	@objcopy \
                --globalize-symbol runtime.g0 \
                --globalize-symbol runtime.m0 \
                --globalize-symbol runtime.physPageSize \
                --globalize-symbol main.main \
		--add-symbol kernel.KKernelEntry=.text:0x`nm build/go.o | grep "main.KKernelEntry$$" | cut -d' ' -f1` \
                 build/go.o build/go.o
	@echo "[$(LD)] linking kernel.bin"
	$(LD) $(LD_FLAGS) -o $@ $(OBJ_FILES)

kernel:build/kernel.bin

clean:
	rm -rf build

qemu:iso
	qemu-system-x86_64 -boot d -cdrom build/kernel.iso -m 512

iso: build/kernel.bin
	rm -rf iso
	mkdir -p iso/boot/grub
	cp $< iso/boot/
	echo 'set timeout=0' >> iso/boot/grub/grub.cfg
	echo 'set default=0' >> iso/boot/grub/grub.cfg
	echo '' >> iso/boot/grub/grub.cfg
	echo 'menuentry "worldos FLK" {' >> iso/boot/grub/grub.cfg
	echo 'multiboot2 /boot/kernel.bin' >> iso/boot/grub/grub.cfg
	echo 'boot' >> iso/boot/grub/grub.cfg
	echo '}' >> iso/boot/grub/grub.cfg
	grub-mkrescue --output=build/kernel.iso iso
	rm -rf iso
vbox-config: | build
	VBoxManage modifyvm "$(VM_NAME)" --uart1 0x3F8 4 --uartmode1 file "$(VBOX_LOG)"

vbox: iso
	@if VBoxManage showvminfo "$(VM_NAME)" --machinereadable | grep -q '^VMState="running"'; then \
		echo "Stopping already-running VM: $(VM_NAME)"; \
		VBoxManage controlvm "$(VM_NAME)" poweroff; \
		while VBoxManage showvminfo "$(VM_NAME)" --machinereadable | grep -q '^VMState="running"'; do sleep 1; done; \
	fi
	$(MAKE) vbox-config
	: > "$(VBOX_LOG)"
	VBoxManage startvm "$(VM_NAME)" --type gui
	@echo "Guest serial log: $(VBOX_LOG)"

vbox-log:
	@if test -f "$(VBOX_LOG)"; then tail -c 4096 "$(VBOX_LOG)"; echo; else echo "No VirtualBox log yet: $(VBOX_LOG)"; fi

diagnose:
	@tools/decode_serial_log.sh "$(VBOX_LOG)" build/kernel.bin
	
