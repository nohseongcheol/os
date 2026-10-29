PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard codiceSorgente/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include spazio_utente/app_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := spazio_utente/dichiarazione/spazio_utente.java ../compiler/START_USER_app.s ../compiler/USER_link_Layout.ld ../compiler/CLR_Supporto.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/CLR_Supporto.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java codiceSorgente/rete_Pila.java build/network-source/rete_Pila.java
	sh $(COMPILER) --target kernel --entry Nucleo.avvia --export kernel_dispatch=chiamata_di_sistema.Processi_VALORE_voce -o $@ $(filter-out codiceSorgente/rete_Pila.java,$(SOURCES)) build/network-source/rete_Pila.java

build/boot.o: avvio_macchina/punto_di_ingresso_VALORE.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE strumenti/자바파일묶기.py | build
	$(PYTHON) strumenti/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: avvio_macchina/spazio_utente.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ spazio_utente/dichiarazione/spazio_utente.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/File_ABI_test.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/datagramma_test.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/STDIN_test.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) spazio_utente/app_f5044b9b.mk strumenti/BIND_endpoint.py
	$(PYTHON) strumenti/BIND_endpoint.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin avvio_macchina/eseguibile_aggregare.s
	$(AS) --32 -o $@ avvio_macchina/eseguibile_aggregare.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o avvio_macchina/disposizione_di_collegamento.ld
	$(LD) -m elf_i386 -T avvio_macchina/disposizione_di_collegamento.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf avvio_macchina/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp avvio_macchina/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: strumenti/Crea_Memoria_supporti.py | build
	$(PYTHON) strumenti/Crea_Memoria_supporti.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) prove/pacchetto_test.py
	$(PYTHON) prove/부팅시험.py
	$(PYTHON) prove/test_Usenet.py
	$(PYTHON) prove/자바시험.py
	$(PYTHON) prove/자바파일시험.py
	$(PYTHON) prove/caso_test.py
	$(PYTHON) prove/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) prove/caso_test.py
	$(PYTHON) prove/보존시험.py
	$(PYTHON) prove/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) prove/자바시험.py
	$(PYTHON) prove/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) prove/test_Usenet.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
