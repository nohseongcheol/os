PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard source/*.java))
COMPILER := ../compiler/tempsDeAnticipé.sh
COMPILER_SOURCES := $(wildcard ../compiler/OutilJava/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include Utilisateur/Programme.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := Utilisateur/Déclarations/Utilisateur.java ../compiler/démarrerProgrammeUtilisateur.s ../compiler/dispositionLierUtilisateur.ld ../compiler/PriseEnChargeEnvironnementExécution.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/PriseEnChargeEnvironnementExécution.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java source/PileRéseau.java build/network-source/PileRéseau.java
	sh $(COMPILER) --target kernel --entry Noyau.lancer --export kernel_dispatch=AppelSystème.entréeÉlémentValeurProcessus -o $@ $(filter-out source/PileRéseau.java,$(SOURCES)) build/network-source/PileRéseau.java

build/boot.o: Amorçage/valeurPointEntréeÉlément.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE Outils/EmballerFichiersJava.py | build
	$(PYTHON) Outils/EmballerFichiersJava.py -o $@ $(JAVA_FILES)

build/user.o: Amorçage/Utilisateur.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ Utilisateur/Déclarations/Utilisateur.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/TestABIFichier.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/TestDatagramme.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/TestEntréeStandard.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/TestPréservationFichier.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) Utilisateur/Programme.mk Outils/EmballerExécutables.py
	$(PYTHON) Outils/EmballerExécutables.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin Amorçage/LotCodeExécutable.s
	$(AS) --32 -o $@ Amorçage/LotCodeExécutable.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o Amorçage/DispositionLiens.ld
	$(LD) -m elf_i386 -T Amorçage/DispositionLiens.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf Amorçage/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp Amorçage/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: Outils/CréerSupportStockage.py | build
	$(PYTHON) Outils/CréerSupportStockage.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Tests/TestPaquet.py
	$(PYTHON) Tests/TestAmorçage.py
	$(PYTHON) Tests/testRéseauUtilisateur.py
	$(PYTHON) Tests/TestJava.py
	$(PYTHON) Tests/TestFichierJava.py
	$(PYTHON) Tests/TestContrat.py
	$(PYTHON) Tests/TestPersistance.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Tests/TestContrat.py
	$(PYTHON) Tests/TestPersistance.py
	$(PYTHON) Tests/TestFichierJava.py

test-java: build/kernel.iso
	$(PYTHON) Tests/TestJava.py
	$(PYTHON) Tests/TestFichierJava.py

test-network: build/kernel.iso
	$(PYTHON) Tests/testRéseauUtilisateur.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
