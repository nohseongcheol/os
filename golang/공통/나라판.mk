세계판뿌리 := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
ENGOS_ROOT ?= /home/user/engos
BUILD_DIR := $(CURDIR)/build
ISO_DIR := $(BUILD_DIR)/iso-root

.PHONY: all kernel iso clean info

all: iso

info:
	@sed -n '1,8p' country.conf

kernel:
	$(MAKE) -C "$(ENGOS_ROOT)" kernel
	mkdir -p "$(BUILD_DIR)"
	cp "$(ENGOS_ROOT)/build/kernel.bin" "$(BUILD_DIR)/kernel.bin"

iso: kernel
	rm -rf "$(ISO_DIR)"
	mkdir -p "$(ISO_DIR)/boot/grub"
	cp "$(BUILD_DIR)/kernel.bin" "$(ISO_DIR)/boot/kernel.bin"
	cp country.conf "$(ISO_DIR)/boot/country.conf"
	echo 'set timeout=0' > "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'set default=0' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'menuentry "WorldOS country [$(COUNTRY_ALPHA3)]" {' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'multiboot2 /boot/kernel.bin' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'module2 /boot/country.conf country' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo 'boot' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	echo '}' >> "$(ISO_DIR)/boot/grub/grub.cfg"
	grub-mkrescue --output="$(BUILD_DIR)/worldos-$(COUNTRY_ALPHA3).iso" "$(ISO_DIR)"
	rm -rf "$(ISO_DIR)"

clean:
	rm -rf "$(BUILD_DIR)"
