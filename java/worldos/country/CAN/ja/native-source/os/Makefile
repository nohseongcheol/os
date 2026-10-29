PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard ソース/*.java))
COMPILER := ../compiler/事前用時間.sh
COMPILER_SOURCES := $(wildcard ../compiler/Java道具/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include 利用者/プログラム.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := 利用者/宣言/利用者.java ../compiler/利用者プログラム開始処理.s ../compiler/利用者連結配置.ld ../compiler/実行環境支援.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/実行環境支援.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java ソース/通信網.java build/network-source/通信網.java
	sh $(COMPILER) --target kernel --entry 中核.起動処理 --export kernel_dispatch=システム呼出.プロセス値入口 -o $@ $(filter-out ソース/通信網.java,$(SOURCES)) build/network-source/通信網.java

build/boot.o: 起動/入口点値.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE 道具/Javaファイル梱包.py | build
	$(PYTHON) 道具/Javaファイル梱包.py -o $@ $(JAVA_FILES)

build/user.o: 起動/利用者.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ 利用者/宣言/利用者.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/ファイルABI試験.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/データグラム試験.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/標準入力試験.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/ファイル保持状態試験.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) 利用者/プログラム.mk 道具/実行束梱包.py
	$(PYTHON) 道具/実行束梱包.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 起動/実行形式束.s
	$(AS) --32 -o $@ 起動/実行形式束.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 起動/連結配置.ld
	$(LD) -m elf_i386 -T 起動/連結配置.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf 起動/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp 起動/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: 道具/記憶媒体作成.py | build
	$(PYTHON) 道具/記憶媒体作成.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 試験/パケット試験.py
	$(PYTHON) 試験/起動試験.py
	$(PYTHON) 試験/利用者通信網試験.py
	$(PYTHON) 試験/Java試験.py
	$(PYTHON) 試験/Javaファイル試験.py
	$(PYTHON) 試験/契約試験.py
	$(PYTHON) 試験/永続化試験.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 試験/契約試験.py
	$(PYTHON) 試験/永続化試験.py
	$(PYTHON) 試験/Javaファイル試験.py

test-java: build/kernel.iso
	$(PYTHON) 試験/Java試験.py
	$(PYTHON) 試験/Javaファイル試験.py

test-network: build/kernel.iso
	$(PYTHON) 試験/利用者通信網試験.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
