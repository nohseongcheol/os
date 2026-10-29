COUNTRY_ALPHA3 := CZE
COUNTRY_ALPHA2 := CZ

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "source" kernel
iso source-iso:
	$(MAKE) -C "source" iso
clean:
	$(MAKE) -C "source" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "interpret_příkazů" all
shell-verify:
	$(MAKE) -C "interpret_příkazů" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-CZE" all
posix-verify:
	$(MAKE) -C "posix-CZE" verify

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
