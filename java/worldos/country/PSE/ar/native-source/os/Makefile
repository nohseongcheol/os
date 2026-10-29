PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard مصدر/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/أدواتجافا/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include فضاء_المستخدم/تطبيق_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := فضاء_المستخدم/إعلان/فضاء_المستخدم.java ../compiler/بدء_مستخدم_تطبيق.s ../compiler/مستخدم_ربط_تخطيط.ld ../compiler/دعمتشغيل.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/دعمتشغيل.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java مصدر/شبكة_رمز.java build/network-source/شبكة_رمز.java
	sh $(COMPILER) --target kernel --entry نواة.تشغيل --export kernel_dispatch=نداء_النظام.عملية_قيمة_إدخال -o $@ $(filter-out مصدر/شبكة_رمز.java,$(SOURCES)) build/network-source/شبكة_رمز.java

build/boot.o: إقلاع_الآلة/نقطة_الإدخال_قيمة.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE أدوات/자바파일묶기.py | build
	$(PYTHON) أدوات/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: إقلاع_الآلة/فضاء_المستخدم.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ فضاء_المستخدم/إعلان/فضاء_المستخدم.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/파일규약시험.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/مخطط_بيانات_يختبر.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/إدخال_قياسي_يختبر.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) فضاء_المستخدم/تطبيق_f5044b9b.mk أدوات/يربط_المشارك.py
	$(PYTHON) أدوات/يربط_المشارك.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin إقلاع_الآلة/실행묶음.s
	$(AS) --32 -o $@ إقلاع_الآلة/실행묶음.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o إقلاع_الآلة/تخطيط_الربط.ld
	$(LD) -m elf_i386 -T إقلاع_الآلة/تخطيط_الربط.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf إقلاع_الآلة/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp إقلاع_الآلة/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: أدوات/فتح_تخزين_وسائط.py | build
	$(PYTHON) أدوات/فتح_تخزين_وسائط.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) اختبارات/حزمة_يختبر.py
	$(PYTHON) اختبارات/부팅시험.py
	$(PYTHON) اختبارات/يختبر_مستخدم_شبكة.py
	$(PYTHON) اختبارات/자바시험.py
	$(PYTHON) اختبارات/자바파일시험.py
	$(PYTHON) اختبارات/عقد_يختبر.py
	$(PYTHON) اختبارات/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) اختبارات/عقد_يختبر.py
	$(PYTHON) اختبارات/보존시험.py
	$(PYTHON) اختبارات/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) اختبارات/자바시험.py
	$(PYTHON) اختبارات/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) اختبارات/يختبر_مستخدم_شبكة.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
