COUNTRY_ALPHA3 := SMR
COUNTRY_ALPHA2 := SM

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "codice-sorgente" kernel
iso source-iso:
	$(MAKE) -C "codice-sorgente" iso
clean:
	$(MAKE) -C "codice-sorgente" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "interprete_dei_comandi" all
shell-verify:
	$(MAKE) -C "interprete_dei_comandi" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-SMR" all
posix-verify:
	$(MAKE) -C "posix-SMR" verify

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
