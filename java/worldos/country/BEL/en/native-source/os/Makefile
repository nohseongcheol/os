PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard source/*.java))
COMPILER := ../compiler/aheadOfTime.sh
COMPILER_SOURCES := $(wildcard ../compiler/JavaTools/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include User/Program.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := User/Declaration/User.java ../compiler/startUserProgram.s ../compiler/userLinkLayout.ld ../compiler/RuntimeSupport.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/RuntimeSupport.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java source/networkStack.java build/network-source/networkStack.java
	sh $(COMPILER) --target kernel --entry Kernel.run --export kernel_dispatch=invokeSystemCall.processValueEntry -o $@ $(filter-out source/networkStack.java,$(SOURCES)) build/network-source/networkStack.java

build/boot.o: machine_boot/entryPointValue.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE tools/bundleJavaFiles.py | build
	$(PYTHON) tools/bundleJavaFiles.py -o $@ $(JAVA_FILES)

build/user.o: machine_boot/User.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ User/Declaration/User.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/FileAbiTest.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/DatagramTest.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/StandardInputTest.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/FilePreservationTest.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) User/Program.mk tools/bindEndpoint.py
	$(PYTHON) tools/bindEndpoint.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin machine_boot/ExecutableBundle.s
	$(AS) --32 -o $@ machine_boot/ExecutableBundle.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o machine_boot/link_layout.ld
	$(LD) -m elf_i386 -T machine_boot/link_layout.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf machine_boot/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp machine_boot/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: tools/createStorageMedia.py | build
	$(PYTHON) tools/createStorageMedia.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) tests/PacketTest.py
	$(PYTHON) tests/testBoot.py
	$(PYTHON) tests/testUserNetwork.py
	$(PYTHON) tests/testJava.py
	$(PYTHON) tests/JavaFileTest.py
	$(PYTHON) tests/ContractTest.py
	$(PYTHON) tests/PreservationTest.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) tests/ContractTest.py
	$(PYTHON) tests/PreservationTest.py
	$(PYTHON) tests/JavaFileTest.py

test-java: build/kernel.iso
	$(PYTHON) tests/testJava.py
	$(PYTHON) tests/JavaFileTest.py

test-network: build/kernel.iso
	$(PYTHON) tests/testUserNetwork.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
