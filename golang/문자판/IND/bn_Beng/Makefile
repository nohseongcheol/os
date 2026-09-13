
# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "আদেশ_ব্যাখ্যাকারী" all
shell-verify:
	$(MAKE) -C "আদেশ_ব্যাখ্যাকারী" verify

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

# WorldOS independent kernel entry
.PHONY: source source-iso
source:
	$(MAKE) -C "source" kernel
source-iso:
	$(MAKE) -C "source" iso
