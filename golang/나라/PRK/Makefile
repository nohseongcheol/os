COUNTRY_ALPHA3 := PRK
COUNTRY_ALPHA2 := KP

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "원문" kernel
iso source-iso:
	$(MAKE) -C "원문" iso
clean:
	$(MAKE) -C "원문" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "명령해석기" all
shell-verify:
	$(MAKE) -C "명령해석기" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-PRK" all
posix-verify:
	$(MAKE) -C "posix-PRK" verify

# BEGIN WorldOS managed VirtualBox launcher
.PHONY: vbox vbox-prepare vbox-status vbox-check
export VBOX_BASE_DISK VBOX_VM_NAME VBOX_TYPE
vbox:
	python3 vbox.py run
vbox-prepare:
	python3 vbox.py prepare
vbox-status:
	python3 vbox.py status
vbox-check:
	python3 vbox.py check
# END WorldOS managed VirtualBox launcher
