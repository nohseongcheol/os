PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard 源代码/*.java))
COMPILER := ../compiler/提前所属时间.sh
COMPILER_SOURCES := $(wildcard ../compiler/Java工具/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include 用户/程序.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := 用户/声明/用户.java ../compiler/开始用户程序.s ../compiler/用户连接导航.ld ../compiler/运行时支持.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/运行时支持.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java 源代码/通信网络.java build/network-source/通信网络.java
	sh $(COMPILER) --target kernel --entry 内核.运行 --export kernel_dispatch=系统调用.进程值条目 -o $@ $(filter-out 源代码/通信网络.java,$(SOURCES)) build/network-source/通信网络.java

build/boot.o: 启动/条目分值.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE 工具集/Java文件打包.py | build
	$(PYTHON) 工具集/Java文件打包.py -o $@ $(JAVA_FILES)

build/user.o: 启动/用户.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ 用户/声明/用户.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/文件ABI测试.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/数据报测试.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/标准输入测试.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/文件保留状态测试.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) 用户/程序.mk 工具集/可执行束打包.py
	$(PYTHON) 工具集/可执行束打包.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin 启动/可执行文件捆绑.s
	$(AS) --32 -o $@ 启动/可执行文件捆绑.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o 启动/链接布局.ld
	$(LD) -m elf_i386 -T 启动/链接布局.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf 启动/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp 启动/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: 工具集/创建存储介质.py | build
	$(PYTHON) 工具集/创建存储介质.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 测试/数据包测试.py
	$(PYTHON) 测试/启动测试.py
	$(PYTHON) 测试/测试用户网络.py
	$(PYTHON) 测试/Java测试.py
	$(PYTHON) 测试/Java文件测试.py
	$(PYTHON) 测试/契约测试.py
	$(PYTHON) 测试/持久化测试.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) 测试/契约测试.py
	$(PYTHON) 测试/持久化测试.py
	$(PYTHON) 测试/Java文件测试.py

test-java: build/kernel.iso
	$(PYTHON) 测试/Java测试.py
	$(PYTHON) 测试/Java文件测试.py

test-network: build/kernel.iso
	$(PYTHON) 测试/测试用户网络.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
