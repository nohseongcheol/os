PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard 原始碼/*.java))
COMPILER := ../compiler/提前所屬時間.sh
COMPILER_SOURCES := $(wildcard ../compiler/Java工具/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include 使用者/程式.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := 使用者/聲明/使用者.java ../compiler/開始用戶程式.s ../compiler/用戶連接導航.ld ../compiler/運行時支持.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/運行時支持.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java 原始碼/通信網絡.java build/network-source/通信網絡.java
	sh $(COMPILER) --target kernel --entry 內核.運行 --export kernel_dispatch=系統呼叫.程序值條目 -o $@ $(filter-out 原始碼/通信網絡.java,$(SOURCES)) build/network-source/通信網絡.java

build/boot.o: 啓動/條目分值.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE 工具集/Java檔案打包.py | build
	$(PYTHON) 工具集/Java檔案打包.py -o $@ $(JAVA_FILES)

build/user.o: 啓動/使用者.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ 使用者/聲明/使用者.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/檔案ABI測試.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/數據報測試.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/標準輸入測試.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/檔案保留狀態測試.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) 使用者/程式.mk 工具集/可執行束打包.py
	$(PYTHON) 工具集/可執行束打包.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 啓動/可執行文件捆綁.s
	$(AS) --32 -o $@ 啓動/可執行文件捆綁.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 啓動/鏈接佈局.ld
	$(LD) -m elf_i386 -T 啓動/鏈接佈局.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf 啓動/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp 啓動/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: 工具集/創建存儲介質.py | build
	$(PYTHON) 工具集/創建存儲介質.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 測試/數據包測試.py
	$(PYTHON) 測試/啓動測試.py
	$(PYTHON) 測試/測試用戶網路.py
	$(PYTHON) 測試/Java測試.py
	$(PYTHON) 測試/Java檔案測試.py
	$(PYTHON) 測試/契約測試.py
	$(PYTHON) 測試/持久化測試.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 測試/契約測試.py
	$(PYTHON) 測試/持久化測試.py
	$(PYTHON) 測試/Java檔案測試.py

test-java: build/kernel.iso
	$(PYTHON) 測試/Java測試.py
	$(PYTHON) 測試/Java檔案測試.py

test-network: build/kernel.iso
	$(PYTHON) 測試/測試用戶網路.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
