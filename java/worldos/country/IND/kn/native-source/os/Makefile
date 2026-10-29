PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard ಮೂಲ/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include ಬಳಕೆದಾರ/ಅಪ್ಲಿ_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := ಬಳಕೆದಾರ/ದೃಢೀಕರಣ/ಬಳಕೆದಾರ.java ../compiler/ಆರಂಭಿಸು_ಬಳಕೆದಾರ_ಅಪ್ಲಿ.s ../compiler/ಬಳಕೆದಾರ_ಜೋಡಣೆ_ಲೇಔಟ್.ld ../compiler/ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java ಮೂಲ/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.java build/network-source/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.java
	sh $(COMPILER) --target kernel --entry ಕರ್ನಲ್.ಚಲಾಯಿಸು_2 --export kernel_dispatch=체계호출.ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ_ನಮೂದು -o $@ $(filter-out ಮೂಲ/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.java,$(SOURCES)) build/network-source/ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್.java

build/boot.o: 부팅/ನಮೂದು_ಬಿಂದು_ಮೌಲ್ಯ.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE ಪರಿಕರಗಳು/자바파일묶기.py | build
	$(PYTHON) ಪರಿಕರಗಳು/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: 부팅/ಬಳಕೆದಾರ.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ ಬಳಕೆದಾರ/ದೃಢೀಕರಣ/ಬಳಕೆದಾರ.java $$(APP_SOURCE_$(1))
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

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) ಬಳಕೆದಾರ/ಅಪ್ಲಿ_f5044b9b.mk ಪರಿಕರಗಳು/묶기.py
	$(PYTHON) ಪರಿಕರಗಳು/묶기.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 부팅/실행묶음.s
	$(AS) --32 -o $@ 부팅/실행묶음.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld
	$(LD) -m elf_i386 -T 부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
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
build/files.img: ಪರಿಕರಗಳು/저장매체만들기.py | build
	$(PYTHON) ಪರಿಕರಗಳು/저장매체만들기.py $@
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
