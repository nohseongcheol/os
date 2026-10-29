PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard исходныйКод/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/СредстваJava/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include пространство_пользователя/программа_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := пространство_пользователя/декларация/пространство_пользователя.java ../compiler/Пуск_пользователь_программа.s ../compiler/пользователь_канал_Макет.ld ../compiler/ПоддержкаВыполнения.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/ПоддержкаВыполнения.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java исходныйКод/сеть_стек.java build/network-source/сеть_стек.java
	sh $(COMPILER) --target kernel --entry Ядро.запустить --export kernel_dispatch=системный_вызов.Процесс_ЗНАЧЕН_ввод -o $@ $(filter-out исходныйКод/сеть_стек.java,$(SOURCES)) build/network-source/сеть_стек.java

build/boot.o: запуск_машины/точка_входа_ЗНАЧЕН.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE инструменты/자바파일묶기.py | build
	$(PYTHON) инструменты/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: запуск_машины/пространство_пользователя.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ пространство_пользователя/декларация/пространство_пользователя.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/файл_ABI_тест.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/датаграмма_тест.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/стандарт_входные_данные_тест.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) пространство_пользователя/программа_f5044b9b.mk инструменты/BIND_участник.py
	$(PYTHON) инструменты/BIND_участник.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin запуск_машины/исполняемый_пакет.s
	$(AS) --32 -o $@ запуск_машины/исполняемый_пакет.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o запуск_машины/схема_компоновки.ld
	$(LD) -m elf_i386 -T запуск_машины/схема_компоновки.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf запуск_машины/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp запуск_машины/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: инструменты/Create_Память_носители.py | build
	$(PYTHON) инструменты/Create_Память_носители.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) испытания/пакет_тест.py
	$(PYTHON) испытания/부팅시험.py
	$(PYTHON) испытания/тест_пользователь_сеть.py
	$(PYTHON) испытания/자바시험.py
	$(PYTHON) испытания/자바파일시험.py
	$(PYTHON) испытания/задание_тест.py
	$(PYTHON) испытания/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) испытания/задание_тест.py
	$(PYTHON) испытания/보존시험.py
	$(PYTHON) испытания/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) испытания/자바시험.py
	$(PYTHON) испытания/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) испытания/тест_пользователь_сеть.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
