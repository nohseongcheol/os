PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard broncode/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include gebruikersruimte/app_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := gebruikersruimte/aangifte/gebruikersruimte.java ../compiler/START_gebruiker_app.s ../compiler/gebruiker_link_Indeling.ld ../compiler/CLR_steun.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/CLR_steun.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java broncode/net_stack.java build/network-source/net_stack.java
	sh $(COMPILER) --target kernel --entry Kern.starten --export kernel_dispatch=systeemaanroep.Proces_WAARDE_invoer -o $@ $(filter-out broncode/net_stack.java,$(SOURCES)) build/network-source/net_stack.java

build/boot.o: machineopstart/beginpunt_WAARDE.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE hulpmiddelen/자바파일묶기.py | build
	$(PYTHON) hulpmiddelen/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: machineopstart/gebruikersruimte.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ gebruikersruimte/aangifte/gebruikersruimte.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/파일규약시험.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/datagram_test.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/STDIN_test.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) gebruikersruimte/app_f5044b9b.mk hulpmiddelen/BIND_eindpunt.py
	$(PYTHON) hulpmiddelen/BIND_eindpunt.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin machineopstart/uitvoerbaar_bundel.s
	$(AS) --32 -o $@ machineopstart/uitvoerbaar_bundel.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o machineopstart/koppelindeling.ld
	$(LD) -m elf_i386 -T machineopstart/koppelindeling.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf machineopstart/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp machineopstart/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: hulpmiddelen/maken_Opslag_Media.py | build
	$(PYTHON) hulpmiddelen/maken_Opslag_Media.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) tests/pakket_test.py
	$(PYTHON) tests/부팅시험.py
	$(PYTHON) tests/test_gebruiker_net.py
	$(PYTHON) tests/자바시험.py
	$(PYTHON) tests/자바파일시험.py
	$(PYTHON) tests/taak_test.py
	$(PYTHON) tests/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) tests/taak_test.py
	$(PYTHON) tests/보존시험.py
	$(PYTHON) tests/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) tests/자바시험.py
	$(PYTHON) tests/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) tests/test_gebruiker_net.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
