PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard zdrojový_soubor/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include uživatelský_prostor/program_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := uživatelský_prostor/deklarace_4f4f026b/uživatelský_prostor.java ../compiler/START_uživatel_program.s ../compiler/uživatel_Odkaz_Navigace.ld ../compiler/CLR_vzpěra.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/CLR_vzpěra.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java zdrojový_soubor/síť_Štos.java build/network-source/síť_Štos.java
	sh $(COMPILER) --target kernel --entry jádro.Spustit_2 --export kernel_dispatch=systémové_volání.Proces_HODNOTA_položka -o $@ $(filter-out zdrojový_soubor/síť_Štos.java,$(SOURCES)) build/network-source/síť_Štos.java

build/boot.o: spuštění_stroje/vstupní_bod_HODNOTA.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE nástroje/자바파일묶기.py | build
	$(PYTHON) nástroje/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: spuštění_stroje/uživatelský_prostor.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ uživatelský_prostor/deklarace_4f4f026b/uživatelský_prostor.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/Soubor_ABI_test.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/datagram_test.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/zařízení_STDIN_test.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) uživatelský_prostor/program_f5044b9b.mk nástroje/vázat_účastník.py
	$(PYTHON) nástroje/vázat_účastník.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin spuštění_stroje/spustitelný_sada.s
	$(AS) --32 -o $@ spuštění_stroje/spustitelný_sada.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o spuštění_stroje/rozvržení_spojování.ld
	$(LD) -m elf_i386 -T spuštění_stroje/rozvržení_spojování.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf spuštění_stroje/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp spuštění_stroje/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: nástroje/Create_médium.py | build
	$(PYTHON) nástroje/Create_médium.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) zkoušky/paket_test.py
	$(PYTHON) zkoušky/부팅시험.py
	$(PYTHON) zkoušky/test_uživatel_síť.py
	$(PYTHON) zkoušky/자바시험.py
	$(PYTHON) zkoušky/자바파일시험.py
	$(PYTHON) zkoušky/případ_test.py
	$(PYTHON) zkoušky/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) zkoušky/případ_test.py
	$(PYTHON) zkoušky/보존시험.py
	$(PYTHON) zkoušky/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) zkoušky/자바시험.py
	$(PYTHON) zkoušky/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) zkoušky/test_uživatel_síť.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
