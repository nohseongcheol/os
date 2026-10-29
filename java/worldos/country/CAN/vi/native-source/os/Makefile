PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard mãNguồn/*.java))
COMPILER := ../compiler/thờiGianCủaTrước.sh
COMPILER_SOURCES := $(wildcard ../compiler/CôngCụJava/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include NgườiDùng/ChươngTrình.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := NgườiDùng/KhaiBáo/NgườiDùng.java ../compiler/bắtChạyChươngTrìnhNgườiDùng.s ../compiler/bốTríLiênKếtNgườiDùng.ld ../compiler/HỗTrợMôiTrườngChạy.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/HỗTrợMôiTrườngChạy.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java mãNguồn/NgănXếpMạng.java build/network-source/NgănXếpMạng.java
	sh $(COMPILER) --target kernel --entry Nhân.chạy --export kernel_dispatch=LờiGọiHệThống.mụcGiáTrịTiếnTrình -o $@ $(filter-out mãNguồn/NgănXếpMạng.java,$(SOURCES)) build/network-source/NgănXếpMạng.java

build/boot.o: KhởiĐộng/giáTrịĐiểmMục.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE CôngCụ/GóiTệpJava.py | build
	$(PYTHON) CôngCụ/GóiTệpJava.py -o $@ $(JAVA_FILES)

build/user.o: KhởiĐộng/NgườiDùng.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ NgườiDùng/KhaiBáo/NgườiDùng.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/ThửABITệp.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/ThửĐiệnDữLiệu.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/ThửĐầuVàoChuẩn.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/ThửViệcGiữNguyênTệp.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) NgườiDùng/ChươngTrình.mk CôngCụ/GóiTệpThựcThi.py
	$(PYTHON) CôngCụ/GóiTệpThựcThi.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin KhởiĐộng/GóiGộpTệpThựcThi.s
	$(AS) --32 -o $@ KhởiĐộng/GóiGộpTệpThựcThi.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o KhởiĐộng/BốTríLiênKết.ld
	$(LD) -m elf_i386 -T KhởiĐộng/BốTríLiênKết.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf KhởiĐộng/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp KhởiĐộng/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: CôngCụ/TạoPhươngTiệnLưu.py | build
	$(PYTHON) CôngCụ/TạoPhươngTiệnLưu.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) KiểmThử/ThửGóiTin.py
	$(PYTHON) KiểmThử/ThửKhởiĐộng.py
	$(PYTHON) KiểmThử/thửMạngNgườiDùng.py
	$(PYTHON) KiểmThử/ThửJava.py
	$(PYTHON) KiểmThử/ThửTệpJava.py
	$(PYTHON) KiểmThử/ThửQuyƯớc.py
	$(PYTHON) KiểmThử/ThửLưuGiữ.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) KiểmThử/ThửQuyƯớc.py
	$(PYTHON) KiểmThử/ThửLưuGiữ.py
	$(PYTHON) KiểmThử/ThửTệpJava.py

test-java: build/kernel.iso
	$(PYTHON) KiểmThử/ThửJava.py
	$(PYTHON) KiểmThử/ThửTệpJava.py

test-network: build/kernel.iso
	$(PYTHON) KiểmThử/thửMạngNgườiDùng.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
