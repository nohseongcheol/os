COUNTRY_ALPHA3 := QAT
COUNTRY_ALPHA2 := QA

.PHONY: all kernel iso clean info source source-iso

all: iso
info:
	@sed -n '1,8p' country.conf
kernel source:
	$(MAKE) -C "النص-المصدري" kernel
iso source-iso:
	$(MAKE) -C "النص-المصدري" iso
clean:
	$(MAKE) -C "النص-المصدري" clean

# WorldOS independent command interpreter
.PHONY: shell shell-verify
shell:
	$(MAKE) -C "مفسر_الأوامر" all
shell-verify:
	$(MAKE) -C "مفسر_الأوامر" verify

# WorldOS independent native POSIX
.PHONY: posix posix-verify
posix:
	$(MAKE) -C "posix-QAT" all
posix-verify:
	$(MAKE) -C "posix-QAT" verify

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
