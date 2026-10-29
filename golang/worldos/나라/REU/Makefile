COUNTRY_ALPHA3 := REU
COUNTRY_ALPHA2 := RE

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "code-source" kernel
iso source-iso:
	$(MAKE) -C "code-source" iso
clean:
	$(MAKE) -C "code-source" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "interpréteur_de_commandes" all
shell-verify:
	$(MAKE) -C "interpréteur_de_commandes" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-REU" all
posix-verify:
	$(MAKE) -C "posix-REU" verify

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
