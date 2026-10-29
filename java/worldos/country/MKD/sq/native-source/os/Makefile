PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard BURIMI/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include përdorues/program_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := përdorues/deklarata/përdorues.java ../compiler/nis_përdorues_program.s ../compiler/përdorues_lidh_Navigimi.ld ../compiler/koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java BURIMI/rrjet_Stivë.java build/network-source/rrjet_Stivë.java
	sh $(COMPILER) --target kernel --entry bërthamë.Ekzekuto --export kernel_dispatch=체계호출.Proces_VALUE_futje -o $@ $(filter-out BURIMI/rrjet_Stivë.java,$(SOURCES)) build/network-source/rrjet_Stivë.java

build/boot.o: 부팅/futje_p_VALUE.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE Mjete/자바파일묶기.py | build
	$(PYTHON) Mjete/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: 부팅/përdorues.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ përdorues/deklarata/përdorues.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/파일규약시험.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/자료전문시험.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/표준입력시험.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) përdorues/program_f5044b9b.mk Mjete/묶기.py
	$(PYTHON) Mjete/묶기.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 부팅/실행묶음.s
	$(AS) --32 -o $@ 부팅/실행묶음.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 부팅/lidh_Navigimi.ld
	$(LD) -m elf_i386 -T 부팅/lidh_Navigimi.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf 부팅/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp 부팅/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: Mjete/저장매체만들기.py | build
	$(PYTHON) Mjete/저장매체만들기.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 시험/패킷시험.py
	$(PYTHON) 시험/부팅시험.py
	$(PYTHON) 시험/사용자통신시험.py
	$(PYTHON) 시험/자바시험.py
	$(PYTHON) 시험/자바파일시험.py
	$(PYTHON) 시험/규약시험.py
	$(PYTHON) 시험/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 시험/규약시험.py
	$(PYTHON) 시험/보존시험.py
	$(PYTHON) 시험/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) 시험/자바시험.py
	$(PYTHON) 시험/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) 시험/사용자통신시험.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
