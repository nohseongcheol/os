PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard Quelltext/*.java))
COMPILER := ../compiler/vorabVonElementZeit.sh
COMPILER_SOURCES := $(wildcard ../compiler/JavaWerkzeug/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include Benutzer/Programm.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := Benutzer/Deklarationen/Benutzer.java ../compiler/benutzerProgrammStarten.s ../compiler/benutzerBindenAnordnung.ld ../compiler/LaufzeitUnterstützung.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/LaufzeitUnterstützung.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java Quelltext/Netzwerkstapel.java build/network-source/Netzwerkstapel.java
	sh $(COMPILER) --target kernel --entry Betriebskern.ausführenVorgang --export kernel_dispatch=Systemaufruf.prozessWertEintrag -o $@ $(filter-out Quelltext/Netzwerkstapel.java,$(SOURCES)) build/network-source/Netzwerkstapel.java

build/boot.o: Startvorgang/eintragPunktWert.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE Werkzeuge/JavaDateienPacken.py | build
	$(PYTHON) Werkzeuge/JavaDateienPacken.py -o $@ $(JAVA_FILES)

build/user.o: Startvorgang/Benutzer.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ Benutzer/Deklarationen/Benutzer.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/DateiABIPrüfung.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/DatagrammPrüfung.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/StandardEingabePrüfung.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/DateiBewahrungPrüfung.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) Benutzer/Programm.mk Werkzeuge/AusführbündelPacken.py
	$(PYTHON) Werkzeuge/AusführbündelPacken.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin Startvorgang/AusführdateiBündel.s
	$(AS) --32 -o $@ Startvorgang/AusführdateiBündel.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o Startvorgang/Bindungsanordnung.ld
	$(LD) -m elf_i386 -T Startvorgang/Bindungsanordnung.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf Startvorgang/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp Startvorgang/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: Werkzeuge/SpeichermediumErstellen.py | build
	$(PYTHON) Werkzeuge/SpeichermediumErstellen.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Prüfungen/PaketPrüfung.py
	$(PYTHON) Prüfungen/Startprüfung.py
	$(PYTHON) Prüfungen/benutzerNetzwerkPrüfung.py
	$(PYTHON) Prüfungen/JavaPrüfung.py
	$(PYTHON) Prüfungen/JavaDateiprüfung.py
	$(PYTHON) Prüfungen/VertragPrüfung.py
	$(PYTHON) Prüfungen/Beständigkeitsprüfung.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Prüfungen/VertragPrüfung.py
	$(PYTHON) Prüfungen/Beständigkeitsprüfung.py
	$(PYTHON) Prüfungen/JavaDateiprüfung.py

test-java: build/kernel.iso
	$(PYTHON) Prüfungen/JavaPrüfung.py
	$(PYTHON) Prüfungen/JavaDateiprüfung.py

test-network: build/kernel.iso
	$(PYTHON) Prüfungen/benutzerNetzwerkPrüfung.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
