COUNTRY_ALPHA3 := JPN
COUNTRY_ALPHA2 := JP

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "原始記述" kernel
iso source-iso:
	$(MAKE) -C "原始記述" iso
clean:
	$(MAKE) -C "原始記述" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "命令解釈器" all
shell-verify:
	$(MAKE) -C "命令解釈器" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-JPN" all
posix-verify:
	$(MAKE) -C "posix-JPN" verify

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
