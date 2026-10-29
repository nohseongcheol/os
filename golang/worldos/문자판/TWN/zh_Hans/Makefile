
# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "命令解释器" all
shell-verify:
	$(MAKE) -C "命令解释器" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-TWN" all
posix-verify:
	$(MAKE) -C "posix-TWN" verify

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
	$(MAKE) -C "源代码" kernel
source-iso:
	$(MAKE) -C "源代码" iso
