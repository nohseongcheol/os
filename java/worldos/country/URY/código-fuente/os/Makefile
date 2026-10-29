PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard fuente/*.java))
COMPILER := ../compiler/tiempoDeAnticipado.sh
COMPILER_SOURCES := $(wildcard ../compiler/HerramientaJava/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include Usuario/Programa.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := Usuario/Declaraciones/Usuario.java ../compiler/iniciarProgramaUsuario.s ../compiler/disposiciónEnlazarUsuario.ld ../compiler/SoporteEntornoEjecución.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/SoporteEntornoEjecución.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java fuente/PilaRed.java build/network-source/PilaRed.java
	sh $(COMPILER) --target kernel --entry Núcleo.ponerEnMarcha --export kernel_dispatch=LlamadaSistema.entradaElementoValorProceso -o $@ $(filter-out fuente/PilaRed.java,$(SOURCES)) build/network-source/PilaRed.java

build/boot.o: Arranque/valorPuntoEntradaElemento.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE Herramientas/EmpaquetarArchivosJava.py | build
	$(PYTHON) Herramientas/EmpaquetarArchivosJava.py -o $@ $(JAVA_FILES)

build/user.o: Arranque/Usuario.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ Usuario/Declaraciones/Usuario.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/PruebaABIArchivo.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/PruebaDatagrama.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/PruebaEntradaEstándar.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/PruebaPreservaciónArchivo.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) Usuario/Programa.mk Herramientas/EmpaquetarEjecutables.py
	$(PYTHON) Herramientas/EmpaquetarEjecutables.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin Arranque/PaqueteCódigoEjecutable.s
	$(AS) --32 -o $@ Arranque/PaqueteCódigoEjecutable.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o Arranque/DisposiciónEnlace.ld
	$(LD) -m elf_i386 -T Arranque/DisposiciónEnlace.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf Arranque/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp Arranque/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: Herramientas/CrearMedioAlmacenamiento.py | build
	$(PYTHON) Herramientas/CrearMedioAlmacenamiento.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Pruebas/PruebaPaqueteDatos.py
	$(PYTHON) Pruebas/PruebaArranque.py
	$(PYTHON) Pruebas/pruebaRedUsuario.py
	$(PYTHON) Pruebas/PruebaJava.py
	$(PYTHON) Pruebas/PruebaArchivoJava.py
	$(PYTHON) Pruebas/PruebaContrato.py
	$(PYTHON) Pruebas/PruebaPersistencia.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) Pruebas/PruebaContrato.py
	$(PYTHON) Pruebas/PruebaPersistencia.py
	$(PYTHON) Pruebas/PruebaArchivoJava.py

test-java: build/kernel.iso
	$(PYTHON) Pruebas/PruebaJava.py
	$(PYTHON) Pruebas/PruebaArchivoJava.py

test-network: build/kernel.iso
	$(PYTHON) Pruebas/pruebaRedUsuario.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
