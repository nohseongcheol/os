PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard códigoFonte/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/FerramentasJava/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include espaço_do_utilizador/app_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := espaço_do_utilizador/declaração/espaço_do_utilizador.java ../compiler/START_usuário_app.s ../compiler/usuário_Link_Layout.ld ../compiler/SuporteExecução.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/SuporteExecução.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java códigoFonte/rede_pilha.java build/network-source/rede_pilha.java
	sh $(COMPILER) --target kernel --entry Núcleo.iniciar --export kernel_dispatch=chamada_ao_sistema.Processo_VALOR_entrada -o $@ $(filter-out códigoFonte/rede_pilha.java,$(SOURCES)) build/network-source/rede_pilha.java

build/boot.o: arranque_da_máquina/ponto_de_entrada_VALOR.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE ferramentas/자바파일묶기.py | build
	$(PYTHON) ferramentas/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: arranque_da_máquina/espaço_do_utilizador.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ espaço_do_utilizador/declaração/espaço_do_utilizador.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/Arquivo_ABI_teste.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/datagrama_teste.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/STDIN_teste.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) espaço_do_utilizador/app_f5044b9b.mk ferramentas/BIND_empresa.py
	$(PYTHON) ferramentas/BIND_empresa.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin arranque_da_máquina/executável_grupo.s
	$(AS) --32 -o $@ arranque_da_máquina/executável_grupo.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o arranque_da_máquina/disposição_de_ligação.ld
	$(LD) -m elf_i386 -T arranque_da_máquina/disposição_de_ligação.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf arranque_da_máquina/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp arranque_da_máquina/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: ferramentas/Criar_Armazenamento_Mídia.py | build
	$(PYTHON) ferramentas/Criar_Armazenamento_Mídia.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) testes/pacote_teste.py
	$(PYTHON) testes/부팅시험.py
	$(PYTHON) testes/teste_Usenet.py
	$(PYTHON) testes/자바시험.py
	$(PYTHON) testes/자바파일시험.py
	$(PYTHON) testes/contrato_teste.py
	$(PYTHON) testes/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) testes/contrato_teste.py
	$(PYTHON) testes/보존시험.py
	$(PYTHON) testes/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) testes/자바시험.py
	$(PYTHON) testes/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) testes/teste_Usenet.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
