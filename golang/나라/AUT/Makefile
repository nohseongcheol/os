COUNTRY_ALPHA3 := AUT
COUNTRY_ALPHA2 := AT

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "Quelltext" kernel
iso source-iso:
	$(MAKE) -C "Quelltext" iso
clean:
	$(MAKE) -C "Quelltext" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "Befehlsauswerter" all
shell-verify:
	$(MAKE) -C "Befehlsauswerter" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-AUT" all
posix-verify:
	$(MAKE) -C "posix-AUT" verify

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
