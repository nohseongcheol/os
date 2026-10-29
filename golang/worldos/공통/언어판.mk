세계판뿌리 := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
ENGOS_ROOT ?= /home/user/engos
BUILD_DIR := $(CURDIR)/build
ISO_DIR := $(BUILD_DIR)/iso-root

.PHONY: all kernel iso clean info

all: iso

info:
	@sed -n '1,8p' locale.conf

kernel:
	$(MAKE) -C "$(ENGOS_ROOT)" kernel
	mkdir -p "$(BUILD_DIR)"
	cp "$(ENGOS_ROOT)/build/kernel.bin" "$(BUILD_DIR)/kernel.bin"

iso: kernel
	rm -rf "$(ISO_DIR)"
	mkdir -p "$(ISO_DIR)/boot/grub"
	cp "$(BUILD_DIR)/kernel.bin" "$(ISO_DIR)/boot/kernel.bin"
	cp locale.conf "$(ISO_DIR)/boot/locale.conf"
	echo 'set timeout=0' > "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'set default=0' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'menuentry "WorldOS language [$(LANGUAGE_CODE)]" {' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'multiboot2 /boot/kernel.bin' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'module2 /boot/locale.conf locale' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'boot' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo '}' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	grub-mkrescue --output="$(BUILD_DIR)/worldos-$(LANGUAGE_CODE).iso" "$(ISO_DIR)"
	rm -rf "$(ISO_DIR)"

clean:
	rm -rf "$(BUILD_DIR)"
