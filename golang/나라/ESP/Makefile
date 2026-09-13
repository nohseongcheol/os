COUNTRY_ALPHA3 := ESP
COUNTRY_ALPHA2 := ES

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "código-fuente" kernel
iso source-iso:
	$(MAKE) -C "código-fuente" iso
clean:
	$(MAKE) -C "código-fuente" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "intérprete_de_órdenes" all
shell-verify:
	$(MAKE) -C "intérprete_de_órdenes" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-ESP" all
posix-verify:
	$(MAKE) -C "posix-ESP" verify

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
