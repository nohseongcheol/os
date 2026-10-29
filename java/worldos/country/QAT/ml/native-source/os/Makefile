PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard ഉറവിടം/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include ഉപയോക്താവ്/പ്രോഗ്രാം_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := ഉപയോക്താവ്/പ്രസ്താവം/ഉപയോക്താവ്.java ../compiler/ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം.s ../compiler/ഉപയോക്താവ്_ലിങ്ക്_ലേഔട്ട്.ld ../compiler/പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java ഉറവിടം/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.java build/network-source/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.java
	sh $(COMPILER) --target kernel --entry കെര്_ണല്.നടപ്പിലാക്കുക --export kernel_dispatch=체계호출.പ്രോസസ്_മൂല്യം_എന്_ട്രി -o $@ $(filter-out ഉറവിടം/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.java,$(SOURCES)) build/network-source/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.java

build/boot.o: 부팅/എന്_ട്രി_പോയിന്_റ്_മൂല്യം.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE ഉപകരണങ്ങൾ/자바파일묶기.py | build
	$(PYTHON) ഉപകരണങ്ങൾ/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: 부팅/ഉപയോക്താവ്.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ ഉപയോക്താവ്/പ്രസ്താവം/ഉപയോക്താവ്.java $$(APP_SOURCE_$(1))
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

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) ഉപയോക്താവ്/പ്രോഗ്രാം_f5044b9b.mk ഉപകരണങ്ങൾ/బైండ్_చేయి_അവസാനബിന്ദു.py
	$(PYTHON) ഉപകരണങ്ങൾ/బైండ్_చేయి_അവസാനബിന്ദു.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 부팅/നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ബണ്ടിൽ.s
	$(AS) --32 -o $@ 부팅/നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ബണ്ടിൽ.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 부팅/ലിങ്ക്_ലേഔട്ട്.ld
	$(LD) -m elf_i386 -T 부팅/ലിങ്ക്_ലേഔട്ട്.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
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
build/files.img: ഉപകരണങ്ങൾ/저장매체만들기.py | build
	$(PYTHON) ഉപകരണങ്ങൾ/저장매체만들기.py $@
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
