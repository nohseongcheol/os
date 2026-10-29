PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard plik_źródłowy/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include przestrzeń_użytkownika/program_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := przestrzeń_użytkownika/deklaracja/przestrzeń_użytkownika.java ../compiler/START_użytkownik_program.s ../compiler/użytkownik_Link_Układ.ld ../compiler/CLR_wsparcie.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/CLR_wsparcie.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java plik_źródłowy/sieć_Stos.java build/network-source/sieć_Stos.java
	sh $(COMPILER) --target kernel --entry jądro.Uruchom_2 --export kernel_dispatch=wywołanie_systemowe.Proces_WARTOŚĆ_wpis -o $@ $(filter-out plik_źródłowy/sieć_Stos.java,$(SOURCES)) build/network-source/sieć_Stos.java

build/boot.o: rozruch_maszyny/punkt_wejścia_WARTOŚĆ.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE narzędzia/자바파일묶기.py | build
	$(PYTHON) narzędzia/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: rozruch_maszyny/przestrzeń_użytkownika.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ przestrzeń_użytkownika/deklaracja/przestrzeń_użytkownika.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/Plik_ABI_test.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/datagram_test.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/STDIN_test.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) przestrzeń_użytkownika/program_f5044b9b.mk narzędzia/BIND_uczestnik.py
	$(PYTHON) narzędzia/BIND_uczestnik.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin rozruch_maszyny/wykonywalny_pakiet.s
	$(AS) --32 -o $@ rozruch_maszyny/wykonywalny_pakiet.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o rozruch_maszyny/układ_konsolidacji.ld
	$(LD) -m elf_i386 -T rozruch_maszyny/układ_konsolidacji.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf rozruch_maszyny/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp rozruch_maszyny/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: narzędzia/Twórca_Pamięć_nośnik.py | build
	$(PYTHON) narzędzia/Twórca_Pamięć_nośnik.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) testy/pakiet_test.py
	$(PYTHON) testy/부팅시험.py
	$(PYTHON) testy/test_użytkownik_sieć.py
	$(PYTHON) testy/자바시험.py
	$(PYTHON) testy/자바파일시험.py
	$(PYTHON) testy/sprawa_test.py
	$(PYTHON) testy/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) testy/sprawa_test.py
	$(PYTHON) testy/보존시험.py
	$(PYTHON) testy/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) testy/자바시험.py
	$(PYTHON) testy/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) testy/test_użytkownik_sieć.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
