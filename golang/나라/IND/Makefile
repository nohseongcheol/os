COUNTRY_ALPHA3 := IND
COUNTRY_ALPHA2 := IN

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "मूल-पाठ" kernel
iso source-iso:
	$(MAKE) -C "मूल-पाठ" iso
clean:
	$(MAKE) -C "मूल-पाठ" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "आदेश_व्याख्याकार" all
shell-verify:
	$(MAKE) -C "आदेश_व्याख्याकार" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-IND" all
posix-verify:
	$(MAKE) -C "posix-IND" verify

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
