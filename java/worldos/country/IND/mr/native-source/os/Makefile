PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard स्रोत/*.java))
COMPILER := ../compiler/आगाऊ_संबंधित_वेळ.sh
COMPILER_SOURCES := $(wildcard ../compiler/जावा_साधने/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include प्रयोक्ता/अनुप्रयोग_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := प्रयोक्ता/घोषणा/प्रयोक्ता.java ../compiler/प्रारंभ_प्रयोक्ता_अनुप्रयोग.s ../compiler/प्रयोक्ता_लिंक_लेआउट.ld ../compiler/सामान्य_भाषा_रनटाइम_समर्थन.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/सामान्य_भाषा_रनटाइम_समर्थन.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java स्रोत/संचारजाळे_स्टॅक.java build/network-source/संचारजाळे_स्टॅक.java
	sh $(COMPILER) --target kernel --entry गाभा.सुरू_करा --export kernel_dispatch=सिस्टम_कॉल_आवाहन.प्रक्रिया_मूल्य_प्रविष्टी -o $@ $(filter-out स्रोत/संचारजाळे_स्टॅक.java,$(SOURCES)) build/network-source/संचारजाळे_स्टॅक.java

build/boot.o: प्रणालीप्रारंभ/प्रविष्टी_गुण_मूल्य.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE साधने/बंडल_जावा_संचिका.py | build
	$(PYTHON) साधने/बंडल_जावा_संचिका.py -o $@ $(JAVA_FILES)

build/user.o: प्रणालीप्रारंभ/प्रयोक्ता.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ प्रयोक्ता/घोषणा/प्रयोक्ता.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/संचिका_द्विमानजोडणी_चाचणी.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/स्वतंत्रसंदेश_चाचणी.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/प्रमाणित_आदान_चाचणी.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/संचिका_जतन_चाचणी.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) प्रयोक्ता/अनुप्रयोग_f5044b9b.mk साधने/बाइंड_करा_संचारटोक.py
	$(PYTHON) साधने/बाइंड_करा_संचारटोक.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin प्रणालीप्रारंभ/निष्पादनीय_बंडल.s
	$(AS) --32 -o $@ प्रणालीप्रारंभ/निष्पादनीय_बंडल.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o प्रणालीप्रारंभ/लिंक_लेआउट.ld
	$(LD) -m elf_i386 -T प्रणालीप्रारंभ/लिंक_लेआउट.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf प्रणालीप्रारंभ/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp प्रणालीप्रारंभ/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: साधने/संग्रह_माध्यमे_तयार_करा.py | build
	$(PYTHON) साधने/संग्रह_माध्यमे_तयार_करा.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) चाचण्या/पॅकेट_चाचणी.py
	$(PYTHON) चाचण्या/प्रणालीप्रारंभ_चाचणी.py
	$(PYTHON) चाचण्या/प्रयोक्ता_संचारजाळे_चाचणी.py
	$(PYTHON) चाचण्या/जावा_चाचणी.py
	$(PYTHON) चाचण्या/जावा_संचिका_चाचणी.py
	$(PYTHON) चाचण्या/काम_चाचणी_7b38e7e1.py
	$(PYTHON) चाचण्या/जतन_चाचणी.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) चाचण्या/काम_चाचणी_7b38e7e1.py
	$(PYTHON) चाचण्या/जतन_चाचणी.py
	$(PYTHON) चाचण्या/जावा_संचिका_चाचणी.py

test-java: build/kernel.iso
	$(PYTHON) चाचण्या/जावा_चाचणी.py
	$(PYTHON) चाचण्या/जावा_संचिका_चाचणी.py

test-network: build/kernel.iso
	$(PYTHON) चाचण्या/प्रयोक्ता_संचारजाळे_चाचणी.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
